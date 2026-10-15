import os
import boto3
import math
import time
from datetime import datetime, timezone

ATHENA_DATABASE = os.environ.get("ATHENA_DATABASE", "default")
ATHENA_TABLE = "weather"
S3_BUCKET = os.environ.get("S3_BUCKET", "sea-routes-back")

athena = None

def run_athena_query(query):
    global athena

    if athena is None:
        athena = boto3.client("athena")
    response = athena.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
            "Database": ATHENA_DATABASE
        },
        ResultConfiguration={
            "OutputLocation": f"s3://{S3_BUCKET}/athena-results/"
        }
    )

    return response["QueryExecutionId"]

def wait_for_query(query_id):
    for attempt in range(60):
        response = athena.get_query_execution(
            QueryExecutionId=query_id
        )

        status = response["QueryExecution"]["Status"]["State"]

        if status == "SUCCEEDED":
            return

        if status in ["FAILED", "CANCELLED"]:
            reason = response["QueryExecution"]["Status"].get(
                "StateChangeReason", "Unknown error"
            )
            raise RuntimeError(f"Athena query failed: {reason}")

        time.sleep(1)
    raise TimeoutError("Athena query timed out after 60 seconds")

def get_query_results(query_id):
    rows = []

    paginator = athena.get_paginator("get_query_results")

    for page in paginator.paginate(QueryExecutionId=query_id):
        rows.extend(page["ResultSet"]["Rows"])

    return rows

def query_weather_history(coordinates, start_time, end_time):
    if not coordinates:
        raise ValueError("Route has no coordinates")
    start_dt = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
    end_dt = datetime.fromisoformat(end_time.replace("Z", "+00:00"))

    start_dt = start_dt.astimezone(timezone.utc)
    end_dt = end_dt.astimezone(timezone.utc)

    if start_dt >= end_dt:
        raise ValueError("Start time must be before end time")

    start_date = start_dt.date()
    end_date = end_dt.date()

    coordinate_conditions = []

    for point in coordinates:
        latitude = float(point["latitude"])
        longitude = float(point["longitude"])

        coordinate_conditions.append(
            f"(w.latitude = {latitude} AND w.longitude = {longitude})"
        )

    coordinates_sql = " OR ".join(coordinate_conditions)
    query = f"""
    SELECT
        w.timestamp,
        w.wind_speed,
        w.wind_direction,
        w.wave_height,
        w.water_temperature,
        w.air_temperature,
        w.cloud_cover
    FROM {ATHENA_TABLE}
    CROSS JOIN UNNEST(records) AS t(w)
    WHERE
        (
            (year || '-' || month || '-' || day)
            BETWEEN '{start_date}' AND '{end_date}'
        )
        AND ({coordinates_sql})
        AND from_iso8601_timestamp(w.timestamp)
            BETWEEN from_iso8601_timestamp('{start_dt.isoformat()}')
            AND from_iso8601_timestamp('{end_dt.isoformat()}')
    """
    query_id = run_athena_query(query)

    wait_for_query(query_id)

    rows = get_query_results(query_id)

    weather_records = []

    for row in rows[1:]:
        values = row["Data"]
        if any(
            "VarCharValue" not in value
            for value in values[1:7]
        ):
            continue

        record = {
            "wind_speed": float(values[1]["VarCharValue"]),
            "wind_direction": float(values[2]["VarCharValue"]),
            "wave_height": float(values[3]["VarCharValue"]),
            "water_temperature": float(values[4]["VarCharValue"]),
            "air_temperature": float(values[5]["VarCharValue"]),
            "cloud_cover": float(values[6]["VarCharValue"]),
        }

        weather_records.append(record)

    return calculate_average_weather(weather_records)

def calculate_average_weather(weather_records):
    if not weather_records:
        return None

    count = len(weather_records)
    sin_sum = sum(
        math.sin(math.radians(r["wind_direction"]))
        for r in weather_records
    )

    cos_sum = sum(
        math.cos(math.radians(r["wind_direction"]))
        for r in weather_records
    )

    if math.hypot(sin_sum, cos_sum) < 1e-10:
        average_direction = None
    else:
        average_direction = (
        math.degrees(math.atan2(sin_sum, cos_sum)) + 360
    ) % 360

    return {
        "wind_speed": sum(r["wind_speed"] for r in weather_records) / count,
        "wave_height": sum(r["wave_height"] for r in weather_records) / count,
        "water_temperature": sum(r["water_temperature"] for r in weather_records) / count,
        "air_temperature": sum(r["air_temperature"] for r in weather_records) / count,
        "cloud_cover": sum(r["cloud_cover"] for r in weather_records) / count,
        "wind_direction": average_direction,
    }

if __name__ == "__main__":
    test_records = [
        {
            "wind_speed": 4.0,
            "wind_direction": 350.0,
            "wave_height": 0.5,
            "water_temperature": 12.0,
            "air_temperature": 10.0,
            "cloud_cover": 60.0,
        },
        {
            "wind_speed": 6.0,
            "wind_direction": 10.0,
            "wave_height": 0.7,
            "water_temperature": 14.0,
            "air_temperature": 12.0,
            "cloud_cover": 80.0,
        },
    ]

    print(calculate_average_weather(test_records))
    print("Empty data test:", calculate_average_weather([]))