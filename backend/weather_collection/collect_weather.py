
import json
from urllib.request import urlopen
from urllib.parse import urlencode
from datetime import datetime, timezone
from save_weather import save_weather
from pathlib import Path

LATITUDE = 60.15
LONGITUDE = 24.92


def fetch_api(base_url, variables, latitude, longitude):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": ",".join(variables),
        "timezone": "GMT"
    }

    if "marine-api" not in base_url:
        params["wind_speed_unit"] = "ms"

    url = base_url + "?" + urlencode(params)

    with urlopen(url, timeout=10) as response:
        return json.load(response)

def load_routes():
    routes = []

    for filepath in Path("local_routes").glob("*.json"):
        with open(filepath, "r", encoding="utf-8") as file:
            routes.append(json.load(file))

    return routes

def collect_weather(latitude, longitude, route_id):
    weather = fetch_api(
        "https://api.open-meteo.com/v1/forecast",
        [
            "temperature_2m",
            "wind_speed_10m",
            "wind_direction_10m",
            "wind_gusts_10m",
            "cloud_cover",
            "weather_code"
            ],
    latitude,
    longitude
)

    marine = fetch_api(
        "https://marine-api.open-meteo.com/v1/marine",
        [
            "wave_height",
            "sea_surface_temperature"
        ],
        latitude,
        longitude
    )

    
    return {
    "route_id": "route_01",
    "latitude": latitude,
    "longitude": longitude,
    "weather_valid_at": weather["current"]["time"] + "Z",
    "marine_valid_at": marine["current"]["time"] + "Z",
    "collected_at": datetime.now(timezone.utc).isoformat(),
    "wind_speed_ms": weather["current"]["wind_speed_10m"],
    "wind_direction_deg": weather["current"]["wind_direction_10m"],
    "wind_gust_ms": weather["current"]["wind_gusts_10m"],
    "air_temperature_c": weather["current"]["temperature_2m"],
    "cloud_cover_percent": weather["current"]["cloud_cover"],
    "weather_code": weather["current"]["weather_code"],
    "wave_height_m": marine["current"]["wave_height"],
    "water_temperature_c": marine["current"]["sea_surface_temperature"],
    "source": "open-meteo",
    "data_type": "forecast"
}




if __name__ == "__main__":
    routes = load_routes()
    results = []

    for route in routes:
        for point in route["coordinates"]:
            result = collect_weather(
                point["latitude"],
                point["longitude"],
                route["route_id"]
            )
            results.append(result)

    filepath = save_weather(results)

    print(f"Collected weather for {len(results)} points")
    print(f"Weather saved to: {filepath}")

