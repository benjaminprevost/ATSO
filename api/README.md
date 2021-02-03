# API ATSO
curl				install

## Usage

Lancer la stack
```
docker-compose up -d
```

Obtenir l'IP de la base de donnée
```
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' api_database_1
```

Connexion à la db
```
psql --host=172.18.0.2 --username=user --dbname=database
```

```sql
CREATE TABLE bme280
(id SERIAL PRIMARY KEY,
datetime TIMESTAMP,
temp DOUBLE PRECISION,
pression DOUBLE PRECISION,
humidite DOUBLE PRECISION,
dbm DOUBLE PRECISION,
wifi DOUBLE PRECISION);
```

Copie à partir de l'hôte
```
psql --host=172.18.0.2 --username=user --dbname=database -c \
"copy bme280 (datetime, temp, pression, humidite, dbm, wifi) from STDIN with delimiter as ';'" < data.csv
```

Copie local (Si l'échantillon est monté dans le conteneur)
```SQL
COPY bme280 FROM '/path/to/csv/data.csv' WITH (FORMAT csv);
```

Structure de l'échantillon `data.csv`
```
datetime, temp, pression, humidité, dbm, wifi
```
