import json
import os
import boto3
from query_weather_history import query_weather_history, calculate_average_weather

S3_BUCKET = os.environ.get("S3_BUCKET", "sea-routes-back")
s3 = None

def load_route(route_id, s3_client=None):
    s3_client = s3_client or boto3.client(
        "s3",
        region_name="us-east-1"
    )

    response = s3_client.get_object(
        Bucket=S3_BUCKET,
        Key=f"routes/{route_id}.json"
    )

    route = json.loads(response["Body"].read())
    return route

def load_statistics(route_id, s3_client=None):
    s3_client = s3_client or boto3.client(
        "s3",
        region_name="us-east-1"
    )

    response = s3_client.get_object(
        Bucket=S3_BUCKET,
        Key=f"route_statistics/{route_id}.json"
    )

    statistics = json.loads(response["Body"].read())
    return statistics

def update_average_rating(statistics, new_rating):
    old_count = statistics["total_ratings"]
    old_average = statistics["average_rating"]

    new_count = old_count + 1
    new_average = (old_average * old_count + new_rating) / new_count

    statistics["total_ratings"] = new_count
    statistics["average_rating"] = new_average

    return statistics

def update_weather_groups(statistics, weather, rating):
    groups = statistics["ratings_across_conditions"]

    if not groups:
        new_group = {
            "average_weather": weather.copy(),
            "average_rating": rating,
            "total_ratings": 1
        }

        groups.append(new_group)

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
    updated_statistics,
    average_weather,
    rating
    )

    print("Updated route statistics:", updated_statistics)

    print("Route:", route_id)
    print("Trip start:", start_time)
    print("Trip end:", end_time)
    print("Rating:", rating)

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Event received"})
    }

if __name__ == "__main__":
    from io import BytesIO

    class FakeS3:
        def get_object(self, Bucket, Key):
            if Key.startswith("route_statistics/"):
                statistics_data = {
                "route_id": "route_01",
                "total_ratings": 2,
                "average_rating": 4.0,
                "ratings_across_conditions": []
            }

                return {
                    "Body": BytesIO(json.dumps(statistics_data).encode("utf-8"))
                }

            print("Requested S3 file:", Key)

            route_data = {
                "route_id": "route_01",
                "coordinates": [
                    {"latitude": 60.17, "longitude": 24.94},
                    {"latitude": 60.18, "longitude": 24.95}
                ]
            }

            return {
                "Body": BytesIO(json.dumps(route_data).encode("utf-8"))
            }

    route = load_route("route_01", FakeS3())
    print("Loaded route:", route)
    original_load_route = load_route

    def fake_load_route(route_id):
        return original_load_route(route_id, FakeS3())

    load_route = fake_load_route

    original_load_statistics = load_statistics

    def fake_load_statistics(route_id):
        return original_load_statistics(route_id, FakeS3())
    load_statistics = fake_load_statistics

    def fake_query_weather_history(coordinates, start_time, end_time):
        print("Fake Athena query for:", coordinates)
        return {
        "wind_speed": 5.0,
        "wind_direction": 0.0,
        "wave_height": 0.6,
        "water_temperature": 13.0,
        "air_temperature": 11.0,
        "cloud_cover": 70.0
    }

    query_weather_history = fake_query_weather_history

    statistics = load_statistics("route_01")
    print("Loaded statistics:", statistics)
    updated_statistics = update_average_rating(statistics, 5)
    print("Updated statistics:", updated_statistics)

    test_event = {
        "route_id": "route_01",
        "start_time": "2026-10-15T12:00:00Z",
        "end_time": "2026-10-15T14:00:00Z",
        "rating": 5
    }

    print(lambda_handler(test_event, None))