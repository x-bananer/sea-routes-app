# TODO: 5.2 This file will contain a helper function for calculating
# the current weather conditions for one route.
#
# The function will:
# 1. Receive the coordinates of the selected route from get_route.py.
# 2. Find and read the latest weather JSON file in the weather/ folder in S3.
# 3. Find the weather at each point of the selected route.
# 4. Check that the weather data is recent and all required points are included.
# 5. Calculate the average wind speed, wave height, water temperature,
#    air temperature and cloud cover for the whole route.
# 6. Calculate the average wind direction using the correct method for angles.
# 7. Return the calculated weather conditions to get_route.py.
#
# (This function reads the latest weather file directly from S3.
# Amazon Athena is only used for historical weather queries.)
