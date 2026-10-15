# S3 Storage Structure

```
Amazon S3
└── SeaRoutes Data
    │
    ├── routes/
    │   ├── route_01.json # Route id becomes a name for a file
    │   ├── route_02.json
    │   └── route_03.json
    │
    ├── ratings/
    │   ├── route_01/
    │   │   ├── rating_id_1.json # Rating id becomes a name for a file
    │   │   └── rating_id_2.json
    │   └── route_02/
    │       └── rating_id_3.json
    │
    ├── route_statistics/
    │   ├── route_01.json
    │   └── route_02.json
    │
    └── weather/ # Year, when data was stored
            └── month=10/ # Month, when data was stored
                └── day=14/ # Day, when data was stored
                    ├── 12-00.json # Time, when data was stored
                    ├── 12-10.json
                    └── 12-20.json
```
