# MongoNews
This repository contains code for loading the files from [AirflowNewsCrawler](https://github.com/NewsPipe/AirflowNewsCrawler) to MongoDB. The implementation dockerized, thus the user does not need to worry about dependencies. Additionally, docker-compose is available to increase the useability for the user.

## Requirement
To use this system, you need to create a `.env` file in which the MongoDB information is available:

```
MONGO_DATABASE_NAME=news
MONGO_ROOT_USER=devroot
MONGO_ROOT_PASSWORD=devroot
MONGOEXPRESS_LOGIN=dev
MONGOEXPRESS_PASSWORD=dev
```

Additionally, you need to change line 15 in the `docker-compose.yml` to the path of the output from [AirflowNewsCrawler](https://github.com/NewsPipe/AirflowNewsCrawler). In my case, the output folder is at `../AirflowNewsCrawler/output/pipelines/`.

## Getting Started
To start this application, run:
```
docker-compose up
docker exec -it mongo python3 /scripts/CSV-to-MongoDB.py
```
To see the database collections, [mongo-express](https://github.com/mongo-express/mongo-express) is in use and available on `localhost:8081`. The MongoDB itself is available on port `27017`. The 

