# TODO: Here will be the first lambda handler function (for data collection). AWS Lambda will run this function every 10 minutes using EventBridge. The function will get all weather data from all weather APIs, check the data and call save_weather.py to save the data to S3. 
# 
# (So we will upload both collect_weather.py and save_weather.py to the same first AWS Lambda function.)