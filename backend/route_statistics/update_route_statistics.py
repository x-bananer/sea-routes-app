import json
import os
import math
from datetime import datetime, timezone

import boto3
from botocore.exceptions import ClientError

from query_weather_history import query_weather_history

S3_BUCKET = os.environ.get("S3_BUCKET", "sea-routes-back")
s3 = None
CORS_HEADERS = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
}

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

    try:
        response = s3_client.get_object(
            Bucket=S3_BUCKET, Key=f"route_statistics/{route_id}.json"
        )
    except ClientError as error:
        if error.response["Error"]["Code"] in ("404", "NoSuchKey", "NotFound"):
            return {
                "route_id": route_id,
                "overall_rating": None,
                "total_ratings": 0,
                "ratings_across_conditions": [],
            }
        raise

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


def get_rating_data(event):
    body = event.get("body", event)
    if isinstance(body, str):
        body = json.loads(body)

    path_parameters = event.get("pathParameters") or {}
    route_id = body.get("route_id") or path_parameters.get("route_id")
    return route_id, body["start_time"], body["end_time"], body["rating"]


def validate_rating(route_id, start_time, end_time, rating):
    if not isinstance(route_id, str) or not route_id.strip():
        raise ValueError("Invalid route ID")
    if type(rating) is not int or not 1 <= rating <= 5:
        raise ValueError("Rating must be an integer from 1 to 5")

    start = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
    end = datetime.fromisoformat(end_time.replace("Z", "+00:00"))
    if start.tzinfo is None or end.tzinfo is None:
        raise ValueError("Trip dates must include a timezone")
    if start >= end:
        raise ValueError("Trip end must be after trip start")
    if end > datetime.now(timezone.utc):
        raise ValueError("Trip cannot end in the future")


def lambda_handler(event, context):
    if event.get("httpMethod") == "OPTIONS":
        return {"statusCode": 204, "headers": CORS_HEADERS, "body": ""}

    try:
        route_id, start_time, end_time, rating = get_rating_data(event)
        validate_rating(route_id, start_time, end_time, rating)

        route = load_route(route_id)
        average_weather = query_weather_history(
            route["coordinates"], start_time, end_time
        )

        statistics = load_statistics(route_id)
        updated_statistics = update_average_rating(statistics, rating)
        updated_statistics = update_weather_groups(
            updated_statistics, average_weather, rating
        )
        save_statistics(route_id, updated_statistics)

        return {
            "statusCode": 200,
            "headers": CORS_HEADERS,
            "body": json.dumps({"message": "Route statistics updated"}),
        }

    except (AttributeError, KeyError, TypeError, ValueError, json.JSONDecodeError):
        return {
            "statusCode": 400,
            "headers": CORS_HEADERS,
            "body": json.dumps({"error": "Invalid rating data"}),
        }

    except ClientError as error:
        if error.response["Error"]["Code"] in ("404", "NoSuchKey", "NotFound"):
            return {
                "statusCode": 404,
                "headers": CORS_HEADERS,
                "body": json.dumps({"error": "Route not found"}),
            }
        print("AWS error:", error)
        return {
            "statusCode": 500,
            "headers": CORS_HEADERS,
            "body": json.dumps({"error": "Failed to update route statistics"}),
        }

    except (RuntimeError, TimeoutError) as error:
        print("Statistics error:", error)
        return {
            "statusCode": 500,
            "headers": CORS_HEADERS,
            "body": json.dumps({"error": "Failed to update route statistics"}),
        }
