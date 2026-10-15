# Data Models

## In S3

`S3: routes/route_01.json`
```json
{
  "id": "route_01",
  "name": "Hietaniemi",
  "coordinates": [
    { "latitude": 60.175, "longitude": 24.912 },
    { "latitude": 60.170, "longitude": 24.895 },
    { "latitude": 60.162, "longitude": 24.880 }
  ]
}
```

`S3: ratings/route_01/rating_id_1.json`
```json
{
  "rating_id": "rating_id_1",
  "route_id": "route_01",
  "start_time": "2026-10-13T12:00:00Z",
  "end_time": "2026-10-13T14:00:00Z",
  "rating": 5
}
```

`S3: weather/year=2026/month=10/day=14/12-00.json`
```json
[
  {
    "timestamp": "2026-10-14T12:00:00Z",
    "latitude": 60.175,
    "longitude": 24.912,
    "wind_speed": 7.2,
    "wind_direction": 220,
    "wave_height": 0.5,
    "water_temperature": 12,
    "air_temperature": 14,
    "cloud_cover": 60
  },
  {
    "timestamp": "2026-10-14T12:00:00Z",
    "latitude": 60.170,
    "longitude": 24.895,
    "wind_speed": 6.5,
    "wind_direction": 215,
    "wave_height": 0.4,
    "water_temperature": 12,
    "air_temperature": 14,
    "cloud_cover": 55
  },
  {
    "timestamp": "2026-10-14T12:00:00Z",
    "latitude": 60.162,
    "longitude": 24.880,
    "wind_speed": 8.1,
    "wind_direction": 230,
    "wave_height": 0.7,
    "water_temperature": 11,
    "air_temperature": 13,
    "cloud_cover": 65
  }
]
```

`S3: route_statistics/route_01.json`
```json
{
  "route_id": "route_01",
  "overall_rating": 4.3,
  "total_ratings": 42,
  "ratings_across_conditions": [
    {
      "weather": {
        "wind_speed": 7.2,
        "wind_direction": 220,
        "wave_height": 0.5,
        "water_temperature": 12,
        "air_temperature": 14,
        "cloud_cover": 60
      },
      "average_rating": 4.8,
      "total_ratings": 12
    },
    {
      "weather": {
        "wind_speed": 3.1,
        "wind_direction": 180,
        "wave_height": 0.2,
        "water_temperature": 11,
        "air_temperature": 10,
        "cloud_cover": 90
      },
      "average_rating": 3.2,
      "total_ratings": 8
    }
  ]
}
```

## For HTTP responses

`HTTP response: GET /routes`
```json
[
  {
    "id": "route_01",
    "name": "Hietaniemi",
    "coordinates": [
      { "latitude": 60.175, "longitude": 24.912 },
      { "latitude": 60.170, "longitude": 24.895 },
      { "latitude": 60.162, "longitude": 24.880 }
    ]
  },
  {
    "id": "route_02",
    "name": "Lauttasaari",
    "coordinates": [
      { "latitude": 60.158, "longitude": 24.882 },
      { "latitude": 60.151, "longitude": 24.874 },
      { "latitude": 60.147, "longitude": 24.865 }
    ]
  }
]
```

`HTTP response: GET /routes/route_01`
```json
{
  "id": "route_01",
  "name": "Hietaniemi",
  "coordinates": [
    { "latitude": 60.175, "longitude": 24.912 },
    { "latitude": 60.170, "longitude": 24.895 },
    { "latitude": 60.162, "longitude": 24.880 }
  ],
  "overall_rating": 4.3,
  "total_ratings": 42,
  "ratings_across_conditions": [
    {
      "weather": {
        "wind_speed": 7.2,
        "wind_direction": 220,
        "wave_height": 0.5,
        "water_temperature": 12,
        "air_temperature": 14,
        "cloud_cover": 60
      },
      "average_rating": 4.8,
      "total_ratings": 12
    },
    {
      "weather": {
        "wind_speed": 3.1,
        "wind_direction": 180,
        "wave_height": 0.2,
        "water_temperature": 11,
        "air_temperature": 10,
        "cloud_cover": 90
      },
      "average_rating": 3.2,
      "total_ratings": 8
    }
  ],
  "current_weather": {
    "wind_speed": 7.27,
    "wind_direction": 222,
    "wave_height": 0.53,
    "water_temperature": 11.67,
    "air_temperature": 13.67,
    "cloud_cover": 60
  },
  "suitability": 4.7
}
```
