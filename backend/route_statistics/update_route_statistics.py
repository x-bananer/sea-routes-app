# TODO: 3.1 Here will be the third Lambda handler function (for updating route statistics).
# The Rating Storage Lambda will call this function asynchronously after saving a new rating.
#
# The function will:
# 1. Receive the new rating, including the route ID, trip start time,
#    trip end time and rating value.
# 2. Read the selected route from the routes/ folder in S3 to get its coordinates.
# 3. Call query_weather_history.py to find the weather at these points
#    during the user's trip.
# 4. Receive the calculated weather conditions for the whole trip.
# 5. Read the existing statistics from route_statistics/{route_id}.json in S3.
# 6. Update the overall average rating and total number of ratings.
# 7. Compare the trip's weather with the existing weather groups
#    in ratings_across_conditions, regardless of the trip date.
# 8. If similar weather conditions are found, update the group's
#    average weather values, average rating and total number of ratings.
#    Otherwise, create a new group.
# 9. Save the updated route statistics to the same JSON file in S3.
#
# (Weather groups do not store trip start or end times. These times
# are only used to find historical weather data for each rating.)
#
# (The function updates aggregated statistics. The original user ratings
# in ratings/ remain unchanged.)
#
# (We will upload both update_route_statistics.py and query_weather_history.py
# to the same AWS Lambda function.)
