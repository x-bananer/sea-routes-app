import json
from datetime import datetime, timezone
import uuid
import os
import boto3
from botocore.exceptions import ClientError

S3_BUCKET = os.environ.get("S3_BUCKET", "sea-routes-back")
UPDATE_STATISTICS_FUNCTION_NAME = "update_route_statistics"
s3 = boto3.client("s3")
lambda_client = boto3.client("lambda")
CORS_HEADERS = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
}


def route_exists(route_id):
    try:
        s3.head_object(Bucket=S3_BUCKET, Key=f"routes/{route_id}.json")
        return True

    except ClientError as error:
        error_code = error.response["Error"]["Code"]

        if error_code in ("404", "NoSuchKey", "NotFound"):
            return False

        raise


def lambda_handler(event, context):
    if event.get("httpMethod") == "OPTIONS":
        return {"statusCode": 204, "headers": CORS_HEADERS, "body": ""}

    try:
        body = event.get("body", event)

        if isinstance(body, str):
            body = json.loads(body)

        route_id = body["route_id"]
        start_time = body["start_time"]
        end_time = body["end_time"]
        rating = body["rating"]

        # Check route ID
        if not isinstance(route_id, str) or not route_id.strip():
            raise ValueError("Invalid route ID")
        # Check if the route exists in S3
        if not route_exists(route_id):
            return {
                "statusCode": 404,
                "headers": CORS_HEADERS,
                "body": json.dumps({"error": "Route not found"}),
            }
        # Check rating (1-5, whole numbers only)
        if type(rating) is not int or not 1 <= rating <= 5:
            raise ValueError("Rating must be an integer from 1 to 5")

        # Check trip dates
        start = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
        end = datetime.fromisoformat(end_time.replace("Z", "+00:00"))

        if start.tzinfo is None or end.tzinfo is None:
            raise ValueError("Trip dates must include a timezone")

        if start >= end:
            raise ValueError("Trip end must be after trip start")

        if end > datetime.now(timezone.utc):
            raise ValueError("Trip cannot end in the future")

        # Generate a unique rating ID
        rating_id = str(uuid.uuid4())

        # Create rating data
        rating_data = {
            "rating_id": rating_id,
            "route_id": route_id,
            "start_time": start_time,
            "end_time": end_time,
            "rating": rating,
        }

        print(json.dumps(rating_data, indent=2))
        s3_key = f"ratings/{route_id}/{rating_id}.json"

        s3.put_object(
            Bucket=S3_BUCKET,
            Key=s3_key,
            Body=json.dumps(rating_data),
            ContentType="application/json",
        )

        lambda_client.invoke(
            FunctionName=UPDATE_STATISTICS_FUNCTION_NAME,
            InvocationType="Event",
            Payload=json.dumps(rating_data).encode("utf-8"),
        )

        print("Route:", route_id)
        print("Start:", start_time)
        print("End:", end_time)
        print("Rating:", rating)

        return {
            "statusCode": 201,
            "headers": CORS_HEADERS,
            "body": json.dumps(
                {"message": "Rating saved successfully", "rating_id": rating_id}
            ),
        }

    except (ClientError, RuntimeError) as error:
        print("AWS error:", error)
        return {
            "statusCode": 500,
            "headers": CORS_HEADERS,
            "body": json.dumps(
                {"error": "Failed to save rating or invoke statistics update"}
            ),
        }

    except (KeyError, TypeError, ValueError, json.JSONDecodeError):
        return {
            "statusCode": 400,
            "headers": CORS_HEADERS,
            "body": json.dumps({"error": "Invalid rating data"}),
        }


if __name__ == "__main__":
    test_event = {
        "body": json.dumps(
            {
                "route_id": "route_01",
                "start_time": "2026-10-13T12:00:00Z",
                "end_time": "2026-10-13T14:00:00Z",
                "rating": 5,
            }
        )
    }
    # Local test: simulate an existing route in S3
    result = lambda_handler(test_event, None)
    print(result)
