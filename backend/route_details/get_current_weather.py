import json
import math
import os
from datetime import datetime, timedelta, timezone

import boto3

S3_BUCKET = os.environ.get("S3_BUCKET", "sea-routes-back")
WEATHER_PREFIX = "weather/"
MAX_WEATHER_AGE_MINUTES = int(os.environ.get("MAX_WEATHER_AGE_MINUTES", "120"))

WEATHER_FIELDS = (
    "wind_speed",
    "wave_height",
    "water_temperature",
    "air_temperature",
    "cloud_cover",
)


def load_latest_weather(s3_client=None):
    s3_client = s3_client or boto3.client("s3")
    latest_object = None

    paginator = s3_client.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=S3_BUCKET, Prefix=WEATHER_PREFIX):
        for item in page.get("Contents", []):
            if not item["Key"].endswith(".json"):
                continue
            if latest_object is None or item["LastModified"] > latest_object["LastModified"]:
                latest_object = item

    if latest_object is None:
        return None, None

    response = s3_client.get_object(Bucket=S3_BUCKET, Key=latest_object["Key"])
    records = json.loads(response["Body"].read().decode("utf-8"))
    return records, latest_object["LastModified"]


def get_current_weather(coordinates, s3_client=None, now=None):
    if not coordinates:
        return None

    records, collected_at = load_latest_weather(s3_client)
    if records is None or not isinstance(records, list):
        return None

    now = now or datetime.now(timezone.utc)
    if collected_at.tzinfo is None:
        collected_at = collected_at.replace(tzinfo=timezone.utc)
    if now - collected_at > timedelta(minutes=MAX_WEATHER_AGE_MINUTES):
        return None

    weather_by_coordinate = {
        (float(record["latitude"]), float(record["longitude"])): record
        for record in records
    }

    route_weather = []
    for point in coordinates:
        record = weather_by_coordinate.get(
            (float(point["latitude"]), float(point["longitude"]))
        )
        if record is None or any(field not in record for field in WEATHER_FIELDS):
            return None
        if "wind_direction" not in record:
            return None
        route_weather.append(record)

    count = len(route_weather)
    average_weather = {
        field: sum(float(record[field]) for record in route_weather) / count
        for field in WEATHER_FIELDS
    }

    sin_sum = sum(
        math.sin(math.radians(float(record["wind_direction"])))
        for record in route_weather
    )
    cos_sum = sum(
        math.cos(math.radians(float(record["wind_direction"])))
        for record in route_weather
    )
    average_weather["wind_direction"] = (
        math.degrees(math.atan2(sin_sum, cos_sum)) + 360
    ) % 360

    return average_weather
