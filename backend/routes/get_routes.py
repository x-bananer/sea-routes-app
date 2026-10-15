import json
import os

import boto3

S3_BUCKET = os.environ.get("S3_BUCKET", "sea-routes-back")
ROUTES_PREFIX = "routes/"
CORS_HEADERS = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
}


def load_routes(s3_client=None):
    routes = []
    s3_client = s3_client or boto3.client("s3")

    paginator = s3_client.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=S3_BUCKET, Prefix=ROUTES_PREFIX):
        for item in page.get("Contents", []):
            key = item["Key"]
            if not key.endswith(".json"):
                continue

            response = s3_client.get_object(Bucket=S3_BUCKET, Key=key)
            routes.append(json.loads(response["Body"].read().decode("utf-8")))

    return routes


def lambda_handler(event, context):
    if event.get("httpMethod") == "OPTIONS":
        return {"statusCode": 204, "headers": CORS_HEADERS, "body": ""}

    return {
        "statusCode": 200,
        "headers": CORS_HEADERS,
        "body": json.dumps(load_routes()),
    }
