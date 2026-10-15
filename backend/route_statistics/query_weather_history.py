# TODO: 3.2 This file will contain a helper function for finding historical
# weather data using Amazon Athena.
#
# The function will:
# 1. Receive the route's coordinates and the user's trip start and end times.
# 2. Create an Athena SQL query to find weather records for these points
#    during the selected time period.
# 3. Use the year, month and day of the trip to search the correct
#    weather data in S3.
# 4. Run the SQL query and wait for the results.
# 5. Calculate the average wind speed, wave height, water temperature,
#    air temperature and cloud cover during the trip.
# 6. Calculate the average wind direction using the correct method
#    for angles.
# 7. Return the calculated weather conditions to update_route_statistics.py.
#
# (Athena will read historical data from the weather/ folder in S3.
# This helper function will not change the weather files.)
