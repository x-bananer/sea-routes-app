
import json
from pathlib import Path
from datetime import datetime, timezone



def save_weather(weather_data):
    # Create a timestamp for this collection
    now = datetime.now(timezone.utc)

    # Create folders by year, month, day and hour
    folder = (
        Path("local_weather")
        / f"year={now.year}"
        / f"month={now.month:02d}"
        / f"day={now.day:02d}"
        / f"hour={now.hour:02d}"
    )

    folder.mkdir(parents=True, exist_ok=True)

    # Save all collected points in one JSON array
    data = (
        weather_data
        if isinstance(weather_data, list)
        else [weather_data]
    )

    filename = now.strftime("%H-%M-%S-%f") + ".json"
    filepath = folder / filename

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)

    return str(filepath)
