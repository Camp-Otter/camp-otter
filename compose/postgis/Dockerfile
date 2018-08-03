FROM mdillon/postgis

# set required environment variables, including states to get
ENV PGUSER=postgres
ENV geostates="'"RI"'"
ENV PGBIN=usr/bin

# install additional dependencies for tiger data
RUN apt-get update
RUN apt-get install -y --no-install-recommends wget unzip zip ca-certificates


# create data folder
RUN mkdir gisdata; mkdir /gisdata/temp; chmod -R 777 /gisdata

# copy files and init database
COPY ./tiger_loader_platform.sql .
COPY init-db.sh .
RUN chmod +x init-db.sh
