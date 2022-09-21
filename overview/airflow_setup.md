# Airflow Setup (Locally via Docker)

All steps to setup Airflow come straight from the offical documentation found [here](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html).

## Fetch the docker-compose.yaml

```curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.4.0/docker-compose.yaml'```
## Setup Environment

### File Directory With root User Ownership

```mkdir -p ./logs ./plugins```

```echo -e "AIRFLOW_UID=$(id -u)" > .env```

### Initialize Airflow Database

```docker-compose up airflow-init```

Login and password are both 'airflow' by default

## Run Airflow

```docker-compose up```

## Airflow UI 

```http://localhost:8080``` using username and password from [Initialization Airflow Database](#initialize-airflow-database)


## Tasks

An outline of the tasks our Airflow DAG will execute can be found [here](./etl.md)

---
[Back to README](../README.md)