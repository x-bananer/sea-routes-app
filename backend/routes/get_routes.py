# TODO: 4.1 Here will be the fourth Lambda handler function (for getting all routes).
# API Gateway will call this function when the frontend sends GET /routes.
#
# The function will:
# 1. Find all JSON files in the routes/ folder in S3.
# 2. Read each file to get the route ID, name and coordinates.
# 3. Combine all routes into one list.
# 4. Return the list as a JSON response to the frontend.
#
# (This function only reads predefined routes from S3.
# It does not calculate weather conditions or route statistics.)
