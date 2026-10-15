import json
import os
import math
import boto3
from query_weather_history import query_weather_history, calculate_average_weather

S3_BUCKET = os.environ.get("S3_BUCKET", "sea-routes-back")
s3 = None

WEATHER_TOLERANCES = {
    "wind_speed": 2.0,
    "wave_height": 0.3,
    "water_temperature": 2.0,
    "air_temperature": 3.0,
    "cloud_cover": 20.0,
}
WIND_DIRECTION_TOLERANCE = 30.0


def load_route(route_id, s3_client=None):
    s3_client = s3_client or boto3.client("s3", region_name="us-east-1")

    response = s3_client.get_object(Bucket=S3_BUCKET, Key=f"routes/{route_id}.json")

    route = json.loads(response["Body"].read())
    return route


def load_statistics(route_id, s3_client=None):
    s3_client = s3_client or boto3.client("s3", region_name="us-east-1")

    response = s3_client.get_object(
        Bucket=S3_BUCKET, Key=f"route_statistics/{route_id}.json"
    )

    statistics = json.loads(response["Body"].read())
    return statistics


def save_statistics(route_id, statistics, s3_client=None):
    s3_client = s3_client or boto3.client("s3", region_name="us-east-1")

    s3_client.put_object(
        Bucket=S3_BUCKET,
        Key=f"route_statistics/{route_id}.json",
        Body=json.dumps(statistics),
        ContentType="application/json",
    )


def update_average_rating(statistics, new_rating):
    old_count = statistics.get("total_ratings", 0)
    old_average = statistics.get("overall_rating") or 0

    new_count = old_count + 1
    new_average = (old_average * old_count + new_rating) / new_count

    statistics["total_ratings"] = new_count
    statistics["overall_rating"] = new_average

    return statistics


def weather_is_similar(group_weather, weather):
    for field, tolerance in WEATHER_TOLERANCES.items():
        if abs(group_weather[field] - weather[field]) > tolerance:
            return False

    direction_difference = abs(
        group_weather["wind_direction"] - weather["wind_direction"]
    )
    direction_difference = min(direction_difference, 360 - direction_difference)

    return direction_difference <= WIND_DIRECTION_TOLERANCE


def update_average_weather(group_weather, weather, old_count):
    new_count = old_count + 1

    for field in WEATHER_TOLERANCES:
        group_weather[field] = (
            group_weather[field] * old_count + weather[field]
        ) / new_count

    old_direction = math.radians(group_weather["wind_direction"])
    new_direction = math.radians(weather["wind_direction"])
    sin_sum = math.sin(old_direction) * old_count + math.sin(new_direction)
    cos_sum = math.cos(old_direction) * old_count + math.cos(new_direction)
    group_weather["wind_direction"] = (
        math.degrees(math.atan2(sin_sum, cos_sum)) + 360
    ) % 360


def update_weather_groups(statistics, weather, rating):
    if weather is None:
        return statistics

    groups = statistics.setdefault("ratings_across_conditions", [])

    for group in groups:
        if weather_is_similar(group["weather"], weather):
            old_count = group["total_ratings"]
            group["total_ratings"] = old_count + 1
            group["average_rating"] = (
                group["average_rating"] * old_count + rating
            ) / group["total_ratings"]
            update_average_weather(group["weather"], weather, old_count)
            return statistics

    groups.append(
        {"weather": weather.copy(), "average_rating": rating, "total_ratings": 1}
    )

    return statistics


def lambda_handler(event, context):
    print("Received event:", event)

    route_id = event["route_id"]
    start_time = event["start_time"]
    end_time = event["end_time"]
    rating = event["rating"]

    route = load_route(route_id)
    coordinates = route["coordinates"]

    print("Route coordinates:", coordinates)
    average_weather = query_weather_history(coordinates, start_time, end_time)

    print("Average weather:", average_weather)
    statistics = load_statistics(route_id)
    updated_statistics = update_average_rating(statistics, rating)

    updated_statistics = update_weather_groups(
        updated_statistics, average_weather, rating
    )

    save_statistics(route_id, updated_statistics)

    print("Updated route statistics:", updated_statistics)

    print("Route:", route_id)
    print("Trip start:", start_time)
    print("Trip end:", end_time)
    print("Rating:", rating)

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Route statistics updated"}),
    }
