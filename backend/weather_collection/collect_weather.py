import json
import os
from urllib.request import urlopen
from urllib.parse import urlencode
import boto3

try:
    from .save_weather import save_weather
except ImportError:
    from save_weather import save_weather

S3_BUCKET = os.environ.get("S3_BUCKET", "sea-routes-back")
ROUTES_PREFIX = "routes/"


def fetch_api(base_url, variables, latitude, longitude):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": ",".join(variables),
        "timezone": "GMT",
    }

    if "marine-api" not in base_url:
        params["wind_speed_unit"] = "ms"

    url = base_url + "?" + urlencode(params)

    with urlopen(url, timeout=10) as response:
        return json.load(response)


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


def collect_weather(points):
    if not points:
        return []

    latitudes = ",".join(str(point["latitude"]) for point in points)
    longitudes = ",".join(str(point["longitude"]) for point in points)

    weather = fetch_api(
        "https://api.open-meteo.com/v1/forecast",
        [
            "temperature_2m",
            "wind_speed_10m",
            "wind_direction_10m",
            "cloud_cover",
        ],
        latitudes,
        longitudes,
    )

    marine = fetch_api(
        "https://marine-api.open-meteo.com/v1/marine",
        ["wave_height", "sea_surface_temperature"],
        latitudes,
        longitudes,
    )

    weather_results = weather if isinstance(weather, list) else [weather]
    marine_results = marine if isinstance(marine, list) else [marine]

    if len(weather_results) != len(points) or len(marine_results) != len(points):
        raise ValueError("Open-Meteo returned an unexpected number of point results")

    return [
        {
            "timestamp": weather_result["current"]["time"] + "Z",
            "latitude": point["latitude"],
            "longitude": point["longitude"],
            "wind_speed": weather_result["current"]["wind_speed_10m"],
            "wind_direction": weather_result["current"]["wind_direction_10m"],
            "wave_height": marine_result["current"]["wave_height"],
            "water_temperature": marine_result["current"]["sea_surface_temperature"],
            "air_temperature": weather_result["current"]["temperature_2m"],
            "cloud_cover": weather_result["current"]["cloud_cover"],
        }
        for point, weather_result, marine_result in zip(
            points, weather_results, marine_results
        )
    ]


def lambda_handler(event, context):
    routes = load_routes()
    points = [point for route in routes for point in route["coordinates"]]
    results = collect_weather(points)
    points_processed = len(points)

    filepath = save_weather(results)

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "routes_processed": len(routes),
                "points_processed": points_processed,
                "s3_path": filepath,
            }
        ),
    }


if __name__ == "__main__":
    print(lambda_handler({}, None)["body"])
