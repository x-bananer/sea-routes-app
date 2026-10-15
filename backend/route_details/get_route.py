import json
import os

import boto3
from botocore.exceptions import ClientError

try:
    from .calculate_conditions_suitability import calculate_conditions_suitability
    from .get_current_weather import get_current_weather
except ImportError:
    from calculate_conditions_suitability import calculate_conditions_suitability
    from get_current_weather import get_current_weather

S3_BUCKET = os.environ.get("S3_BUCKET", "sea-routes-back")
CORS_HEADERS = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
}


def load_json(key, s3_client):
    response = s3_client.get_object(Bucket=S3_BUCKET, Key=key)
    return json.loads(response["Body"].read().decode("utf-8"))


def empty_statistics(route_id):
    return {
        "route_id": route_id,
        "overall_rating": None,
        "total_ratings": 0,
        "ratings_across_conditions": [],
    }


def load_route_statistics(route_id, s3_client):
    try:
        return load_json(f"route_statistics/{route_id}.json", s3_client)
    except ClientError as error:
        if error.response["Error"]["Code"] in ("404", "NoSuchKey", "NotFound"):
            return empty_statistics(route_id)
        raise


def get_route_id(event):
    path_parameters = event.get("pathParameters") or {}
    return path_parameters.get("route_id") or event.get("route_id")


def lambda_handler(event, context):
    if event.get("httpMethod") == "OPTIONS":
        return {"statusCode": 204, "headers": CORS_HEADERS, "body": ""}

    route_id = get_route_id(event)
    if not route_id:
        return {
            "statusCode": 400,
            "headers": CORS_HEADERS,
            "body": json.dumps({"error": "Route ID is required"}),
        }

    s3_client = boto3.client("s3")

    try:
        route = load_json(f"routes/{route_id}.json", s3_client)
    except ClientError as error:
        if error.response["Error"]["Code"] in ("404", "NoSuchKey", "NotFound"):
            return {
                "statusCode": 404,
                "headers": CORS_HEADERS,
                "body": json.dumps({"error": "Route not found"}),
            }
        raise

    try:
        statistics = load_route_statistics(route_id, s3_client)
        current_weather = get_current_weather(route["coordinates"], s3_client)
        suitability = calculate_conditions_suitability(
            current_weather, statistics["ratings_across_conditions"]
        )
    except (ClientError, ValueError, KeyError, TypeError) as error:
        print("Failed to load route details:", error)
        return {
            "statusCode": 500,
            "headers": CORS_HEADERS,
            "body": json.dumps({"error": "Failed to load route details"}),
        }

    response = {
        "id": route.get("id", route_id),
        "name": route["name"],
        "coordinates": route["coordinates"],
        "overall_rating": statistics.get("overall_rating"),
        "total_ratings": statistics.get("total_ratings", 0),
        "ratings_across_conditions": statistics.get(
            "ratings_across_conditions", []
        ),
        "current_weather": current_weather,
        "suitability": suitability,
    }

    return {
        "statusCode": 200,
        "headers": CORS_HEADERS,
        "body": json.dumps(response),
    }
