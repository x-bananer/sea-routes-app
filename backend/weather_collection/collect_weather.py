# TODO: 1.1 Here will be the first Lambda handler function (for weather collection). AWS Lambda will run this function every 10 minutes using EventBridge.
#
# The function will:
# 1. Read all predefined routes from the routes/ folder in S3.
# 2. Get coordinates of all points from these routes and remove duplicate points.
# 3. Request weather data from external APIs for each unique point.
# 4. Check that the received data contains the required weather values.
# 5. Convert the data from different APIs into one common format.
# 6. Call save_weather.py to save the collected data to S3.
#
# (We will upload both collect_weather.py and save_weather.py to the same AWS Lambda function.)