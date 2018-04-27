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

Spin up a database container with the command:
```shell
docker run --name django-postgis -e POSTGRES_PASSWORD=testdjango -p:8080::5432 -d mdillon/postgis
```

Connect to the server to create the database:
```shell
docker run -it --link django-postgis:postgres postgres psql -h postgres -U postgres
```
and the password from above. (This password can also be set using the `POSTGIS_PASSWORD` environment variable.)

Once you're logged in, create the database:
```sql
CREATE DATABASE geodjango;
\q
```

Verify that the settings in `config.setting.base` match what you configured, then everything should be good to go.

## Contributing
This project is under development.  To contribute, visit the [wiki](https://github.com/Camp-Otter/camp-otter/wiki).

Use the [development branch](https://github.com/Camp-Otter/camp-otter/tree/development) to contribute code.