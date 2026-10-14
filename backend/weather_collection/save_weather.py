# TODO: 1.2 Here we will have a helper function for saving collected weather data to S3.
#
# The function will:
# 1. Receive the weather data from collect_weather.py.
# 2. Create one JSON array containing weather data for all unique points.
# 3. Include the timestamp, latitude, longitude, wind speed, wind direction,
#    wave height, water temperature, air temperature and cloud cover for each point.
# 4. Save the JSON array as one file in weather/year={current year}/month={current month}/day={current dat}/{current hour-current minutes}.json in S3.
# 5. Organize files by year, month and day.
# 6. Use the collection time as the file name, for example 12-10.json.
#
# (Every 10 minutes, a new JSON file will be created. Each file will contain
# weather data for all existing points, not just one point.)