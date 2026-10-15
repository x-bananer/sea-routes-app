WEATHER_TOLERANCES = {
    "wind_speed": 2.0,
    "wave_height": 0.3,
    "water_temperature": 2.0,
    "air_temperature": 3.0,
    "cloud_cover": 20.0,
}
WIND_DIRECTION_TOLERANCE = 30.0
MINIMUM_RATINGS = 3


def weather_similarity(current_weather, historical_weather):
    similarities = []

    for field, tolerance in WEATHER_TOLERANCES.items():
        difference = abs(current_weather[field] - historical_weather[field])
        similarities.append(max(0, 1 - difference / tolerance))

    direction_difference = abs(
        current_weather["wind_direction"] - historical_weather["wind_direction"]
    )
    direction_difference = min(direction_difference, 360 - direction_difference)
    similarities.append(max(0, 1 - direction_difference / WIND_DIRECTION_TOLERANCE))

    return sum(similarities) / len(similarities)


def calculate_conditions_suitability(current_weather, rating_groups):
    if not current_weather or not rating_groups:
        return None

    if sum(group.get("total_ratings", 0) for group in rating_groups) < MINIMUM_RATINGS:
        return None

    weighted_ratings = 0
    total_weight = 0

    for group in rating_groups:
        similarity = weather_similarity(current_weather, group["weather"])
        weight = similarity * group["total_ratings"]
        weighted_ratings += group["average_rating"] * weight
        total_weight += weight

    if total_weight == 0:
        return None

    return round(max(1, min(5, weighted_ratings / total_weight)), 1)
