# S3 Storage Structure

```
Amazon S3
└── SeaRoutes Data
    │
    ├── routes/
    │   ├── route_id_1.json # Route id becomes a name for a file
    │   ├── route_id_2.json
    │   └── route_id_3.json
    │
    ├── ratings/
    │   ├── route_id_1/
    │   │   ├── rating_id_1.json # Rating id becomes a name for a file
    │   │   └── rating_id_2.json
    │   └── route_id_2/
    │       └── rating_id_3.json
    │
    ├── route_statistics/
    │   ├── route_id_1.json
    │   └── route_id_2.json
    │
    └── weather/ # Year, when data was stored
            └── month=10/ # Month, when data was stored
                └── day=14/ # Day, when data was stored
                    ├── 12-00.json # Time, when data was stored
                    ├── 12-10.json
                    └── 12-20.json
```
