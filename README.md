# Sea Routes

## Architecture

![AWS Architecture](docs/aws_diagram.png)

## Documentation

- [S3 Storage Structure](docs/s3_structure.md)
- [Data Models and API Responses](docs/data_models.md)
- [Figma Design](https://www.figma.com/design/UktWhTybDFUz3Y86jBLeYi/Untitled?node-id=0-1&t=FIFm8Y7k7JRfBzfS-1)

## Repo Structure Diagram

```
SeaRoutes/
│
├── backend/
│   │
│   ├── weather_collection/                # Lambda 1: Weather Collection
│   │   ├── collect_weather.py             # Gets routes coordinates and requests weather data for them from external APIs
│   │   └── save_weather.py                # Formats weather data and saves it to S3
│   │
│   ├── ratings/                           # Lambda 2: Rating Storage
│   │   └── save_rating.py                 # Saves a user rating to S3 and asynchronously invokes the statistics Lambda
│   │
│   ├── route_statistics/                  # Lambda 3: Route Statistics Update
│   │   ├── update_route_statistics.py     # Calculates aggregated route statistics based on user ratings and historical weather data, then saves them to S3
│   │   └── query_weather_history.py       # Queries historical weather data from S3 using Amazon Athena
│   │
│   ├── routes/                            # Lambda 4: Route List Retrieval
│   │   └── get_routes.py                  # Reads all predefined routes from S3
│   │
│   ├── route_details/                     # Lambda 5: Route Details Retrieval
│       ├── get_route.py                   # Reads route, weather and statistics data and returns route details
│       ├── get_current_weather.py         # Reads the latest weather data from S3, finds the weather at each point of the selected route, and calculates average weather conditions for the whole route
│       └── calculate_conditions_suitability.py # Compares current weather with past ratings and calculates suitability (expected rating)
│   │
│   ├── tests/
│   │   ├── test_collect_weather.py
│   │   ├── test_save_weather.py
│   │   ├── test_save_rating.py
│   │   ├── test_update_route_statistics.py
│   │   ├── test_query_weather_history.py
│   │   ├── test_get_routes.py
│   │   ├── test_get_route.py
│   │   ├── test_get_current_weather.py
│   │   └── test_calculate_conditions_suitability.py
│   │
│   └── requirements.txt                   # Python dependencies
│
├── sql/
│   └── create_weather_table.sql           # Defines the Amazon Athena table for historical weather queries
└── README.md
```
