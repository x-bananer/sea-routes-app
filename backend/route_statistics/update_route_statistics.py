import json
import os
import boto3
from query_weather_history import query_weather_history, calculate_average_weather

S3_BUCKET = os.environ.get("S3_BUCKET", "sea-routes-back")
s3 = None


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


def update_weather_groups(statistics, weather, rating):
    if weather is None:
        return statistics

    groups = statistics.setdefault("ratings_across_conditions", [])

    for group in groups:
        if group["weather"] == weather:
            old_count = group["total_ratings"]
            group["total_ratings"] = old_count + 1
            group["average_rating"] = (
                group["average_rating"] * old_count + rating
            ) / group["total_ratings"]
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
