
import json
import os
from datetime import datetime, timezone
import boto3

S3_BUCKET = os.environ.get("S3_BUCKET", "sea-routes-back")
WEATHER_PREFIX = "weather"


def save_weather(weather_data, s3_client=None):
    # Create a timestamp for this collection
    now = datetime.now(timezone.utc)

    # Save all collected points in one JSON array
    data = (
        weather_data
        if isinstance(weather_data, list)
        else [weather_data]
    )

    filename = now.strftime("%H-%M") + ".json"
    key = (
        f"{WEATHER_PREFIX}/year={now.year}/month={now.month:02d}/"
        f"day={now.day:02d}/hour={now.hour:02d}/{filename}"
    )

    s3_client = s3_client or boto3.client("s3")
    s3_client.put_object(
        Bucket=S3_BUCKET,
        Key=key,
        Body=json.dumps(data).encode("utf-8"),
        ContentType="application/json",
    )

    return f"s3://{S3_BUCKET}/{key}"
