# docker-airflow
[![CI status](https://github.com/puckel/docker-airflow/workflows/CI/badge.svg?branch=master)](https://github.com/puckel/docker-airflow/actions?query=workflow%3ACI+branch%3Amaster+event%3Apush)

This repository contains a **Dockerfile** for running [Apache Airflow](https://airflow.apache.org/) locally using Docker and Docker Compose.

> **Updated:** Upgraded to **Apache Airflow 2.10.3** on **Python 3.11**, with PostgreSQL 13 backend and authentication disabled for local development.

---

## Stack

| Component  | Version              |
|------------|----------------------|
| Python     | 3.11 (slim-bullseye) |
| Airflow    | 2.10.3               |
| PostgreSQL | 13                   |
| Docker     | Latest               |

---

## Prerequisites

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/install/)

---

## Build

Build the local Docker image:

    docker build --rm -t puckel/docker-airflow:local .

Optionally install extra Airflow packages or Python dependencies at build time:

    docker build --rm --build-arg AIRFLOW_DEPS="datadog,dask" -t puckel/docker-airflow:local .
    docker build --rm --build-arg PYTHON_DEPS="flask_oauthlib>=0.9" -t puckel/docker-airflow:local .

---

## Usage

### LocalExecutor (Recommended for local development)

    docker-compose -f docker-compose-LocalExecutor.yml up -d

This starts:
- **PostgreSQL 13** — metadata database
- **Airflow Webserver** — UI at [http://localhost:8080](http://localhost:8080)
- **Airflow Scheduler** — runs automatically inside the webserver container

### CeleryExecutor

    docker-compose -f docker-compose-CeleryExecutor.yml up -d

### Standalone (SequentialExecutor)

    docker run -d -p 8080:8080 puckel/docker-airflow:local webserver

---

## Authentication

Authentication is **disabled** for local development. The Airflow UI at [http://localhost:8080](http://localhost:8080) is accessible directly without any login prompt.

This is controlled by `config/webserver_config.py`:

```python
AUTH_ROLE_PUBLIC = 'Admin'
```

> ⚠️ **Warning:** Do **not** use this configuration in production or on a publicly accessible network.

---

## Load Example DAGs

By default, example DAGs are disabled. To enable them, set the environment variable:

    docker run -d -p 8080:8080 -e LOAD_EX=y puckel/docker-airflow:local

---

## Configuring Airflow

Configuration is managed via `config/airflow.cfg`, which is baked into the Docker image at build time.

You can also override any configuration setting using environment variables in the format:

    AIRFLOW__<SECTION>__<KEY>

Example:

    AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres/airflow

See the [Airflow documentation](https://airflow.apache.org/docs/apache-airflow/stable/howto/set-config.html) for details.

---

## Custom Python Packages

- Add your dependencies to `requirements.txt`
- The file is mounted as a volume in the compose files and installed automatically on startup

---

## Custom Plugins

Place custom plugins in a `plugins/` folder and mount it as a volume:

    -v $(pwd)/plugins/:/usr/local/airflow/plugins

Or uncomment the volume line in `docker-compose-LocalExecutor.yml`.

---

## Database Configuration (PostgreSQL)

The following environment variables configure the PostgreSQL connection:

| Variable            | Default value | Role                 |
|---------------------|---------------|----------------------|
| `POSTGRES_HOST`     | `postgres`    | Database server host |
| `POSTGRES_PORT`     | `5432`        | Database server port |
| `POSTGRES_USER`     | `airflow`     | Database user        |
| `POSTGRES_PASSWORD` | `airflow`     | Database password    |
| `POSTGRES_DB`       | `airflow`     | Database name        |
| `POSTGRES_EXTRAS`   | empty         | Extras parameters    |

---

## Celery Broker Configuration (Redis)

For **CeleryExecutor**, the following Redis environment variables are used:

| Variable         | Default value | Role                           |
|------------------|---------------|--------------------------------|
| `REDIS_PROTO`    | `redis://`    | Protocol                       |
| `REDIS_HOST`     | `redis`       | Redis server host              |
| `REDIS_PORT`     | `6379`        | Redis server port              |
| `REDIS_PASSWORD` | empty         | If Redis is password protected |
| `REDIS_DBNUM`    | `1`           | Database number                |

---

## UI Links

- **Airflow UI:** [http://localhost:8080](http://localhost:8080)
- **Flower (Celery monitor):** [http://localhost:5555](http://localhost:5555)

---

## Running Airflow Commands

Run any Airflow CLI command inside the running container:

    docker exec -it docker-airflow-master-webserver-1 airflow dags list

Start a bash shell:

    docker run --rm -ti puckel/docker-airflow:local bash

---

## Shutting Down

    docker-compose -f docker-compose-LocalExecutor.yml down
