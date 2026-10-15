# SeaRoutes

SeaRoutes helps people choose sea routes in Helsinki. It is for sailboarders,
kayakers, windsurfers, and other people who enjoy being on the water.

Most apps show a map and a weather forecast. SeaRoutes also shows how other
people rated a route in similar weather. This can help users choose a route
they may enjoy.

## Features

- See Helsinki sea routes on a map.
- Check route weather and user ratings.
- Rate a route after a trip.
- See ratings from trips with similar weather.
- Get a route suitability score from 1 to 5 when there is enough data.

## How it works

SeaRoutes gets weather data from Open-Meteo for every point on a route. The
data is saved in Amazon S3.

After a trip, a user can rate a route. The rating and trip time are saved in
S3. A Lambda function uses historical weather data from Athena to update route
statistics.

When a user opens route details, SeaRoutes reads the latest weather data and
route statistics. It compares current weather with past ratings and returns a
suitability score when possible.

## AWS architecture

![SeaRoutes AWS architecture](docs/aws_diagram.png)

## Tech stack

- React, Vite, React Leaflet, Leaflet
- Python and AWS Lambda
- Amazon S3, API Gateway, and Athena
- Open-Meteo Weather API and Marine API

## Run the frontend

```bash
cd frontend
npm install
npm run dev
```

Build files for S3 hosting:

```bash
cd frontend
npm run build
```

The build files are in `frontend/dist/`.

## Team

- Grigorii Tishchuk
- Polina Movshina
- Yaroslav Murykin
- Kseniia Shlenskaia
