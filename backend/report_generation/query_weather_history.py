# TODO: Here will be the function that gets our saved historical weather data from S3 using AWS Athena and SQL queries. It will find weather data for the selected route (coordinates) and time period. Athena runs SQL queries asynchronously, so the function will send a query to Athena, wait until Athena finishes it and return the results to generate_report.py. If the query fails or takes too long, the function will return an error.
#
# (We will upload both generate_report.py and query_weather_history.py to the same second AWS Lambda function.)

