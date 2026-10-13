# TODO: Here will be the second lambda handler function (for report generation). AWS Lambda will run this function when API Gateway gets a request from the frontend. The function will check the selected route (coordinates) and time period, call query_weather_history.py to get weather data stored in our history, wait for it and then return the report to the frontend in JSON format.
#
# (So we will upload both generate_report.py and query_weather_history.py to the same second AWS Lambda function.)
#
# About API Gateway (AI generated): Open AWS Console, go to API Gateway and create an HTTP API. Connect it to the AWS Lambda function that contains both Python files from the report_generation folder (generate_report.py and query_weather_history.py). Create a route for this Lambda. Enable CORS, copy the API URL and use it in frontend to send requests. Documentation: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html
