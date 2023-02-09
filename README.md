# STEP
This a simple project to allow a webservice that processes the image.
## Installation
The project user [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/).

To install Docker, follow the instructions in the [Docker documentation](https://docs.docker.com/engine/installation/).

## Usage
To run the project create a `.env` file in the root directory of the project, use the `.env-copy` file as a template.

To build the project:
```bash
docker-compose build
```
Install alembic to manage the database migrations:
```bash
pip install alembic
```
Start the project:
```bash
docker-compose up
```

To run the migrations:
```bash
alembic upgrade head
```

The project uses [minio](https://min.io/) as a storage service. Create a bucket in minio which is accessible at `http://localhost:9000` with the credentials and name in the `.env` file.

The project is accessible at `http://localhost:8000`.



## Development
The project uses poetry to manage the dependencies. To install the dependencies, run:
```bash
poetry install
```

Use docker compose to build the project:
```bash
docker-compose build
```

To run the project:
```bash
docker-compose up
```

The project uses pre-commit to run the linters and formatters. To install the pre-commit hooks, run:
```bash
pre-commit install
```
