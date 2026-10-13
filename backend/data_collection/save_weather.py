# TODO: Here will be the function that gets weather data from collect_weather.py, creates JSON files with this data and uploads them to AWS S3. 
#
# All JSON files should have the same fields so we can read them with SQL and Athena later. Maybe we could also organize files by date in their name? In this case, it would be easier for us to find them.
#
# (We will upload both collect_weather.py and save_weather.py to the same AWS Lambda function.)