# TODO: 2.1 Here will be the second Lambda handler function (for saving user ratings).
# API Gateway will call this function when a user submits a rating.
#
# The function will:
# 1. Receive the route ID, trip start time, trip end time and rating (1–5).
# 2. Check that the route exists and the received values are valid.
# 3. Generate a unique ID for the new rating.
# 4. Create a JSON object containing the rating ID, route ID, start time,
#    end time and rating.
# 5. Save the JSON file to ratings/{route_id}/{rating_id}.json in S3.
# 6. Asynchronously (!) call the Route Statistics Update Lambda and pass
#    the new rating to it.
# 7. Without waiting for the answer from third Lambda immediately return a response confirming that the rating was saved.
#
# (The statistics update will run separately, so the user will not have
# to wait for it to finish.)