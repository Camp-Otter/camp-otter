# camp-otter

[![Updates](https://pyup.io/repos/github/Camp-Otter/camp-otter/shield.svg)](https://pyup.io/repos/github/Camp-Otter/camp-otter/)

An open source campaign management app written in python using Django.

## Installation

### GeoDjango
The app uses Django's build in GIS system, geodjango. See the documentation for [setup details](https://docs.djangoproject.com/en/2.0/ref/contrib/gis/install/)

### Docker Database
A dockerfile with PostGIS can be used for the geospatial database, simplifying some of the setup.
**CAUTION: don't use in deployment! This setup does not persist data outside the container!**

First, install [Docker](https://www.docker.com/).

Spin up a database container and initialize the db with the commands:
```shell
docker run --name django-postgis -e POSTGRES_PASSWORD=testdjango -p:8080:5432 -d paulopperman/docker-postgis-tiger:0.5
docker exec -it django-postgis ./init-db.sh
```

Verify that the settings in `config.setting.base` match what you configured, then everything should be good to go.

## Testing
The app uses a custom test runner to allow the tiger database functionality to be tested.  This executes tests on the live
database.  All tiger operations should be read only.

## Contributing
This project is under development.  To contribute, visit the [wiki](https://github.com/Camp-Otter/camp-otter/wiki).

Use the [development branch](https://github.com/Camp-Otter/camp-otter/tree/development) to contribute code.