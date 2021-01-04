# API ATSO
curl				install

## Usage

docker-compose up -d


docker-compose run database bash
psql --host=database --username=unicorn_user --dbname=rainbow_database

rainbow_database=# SELECT * FROM color_table; -- verify record does not already exist




docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' container_name_or_id



data.csv

datetime, temp, pression, humidité, dbm, wifi



```sql
CREATE TABLE bme280
(datetime CHAR(255),
temp CHAR(255),
pression CHAR(255),
humidite CHAR(255),
dbm CHAR(255),
wifi CHAR(255));
```

Local copy
```SQL
COPY zip_codes FROM '/path/to/csv/ZIP_CODES.txt' WITH (FORMAT csv);
```

Remote copy

psql --host=172.18.0.2 --username=unicorn_user --dbname=rainbow_database -c \
"copy bme280 (datetime, temp, pression, humidite, dbm, wifi) from STDIN with delimiter as ';'" < data.csv


csv
