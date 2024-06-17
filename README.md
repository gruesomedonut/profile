# FastAPI Starter Kit

## VSCode Dev setup
```bash
pip install poetry==1.5.1
poetry install
poetry shell
# copy virtualenv python path and set it in vscode `Python: Select Interpreter`
# Setup Pre-commit
pre-commit install
pre-commit install --hook-type commit-msg
```

## Features

- **FastAPI** with Python 3.11
- **PostgreSQL 15**
- **SQLAlchemy** with Alembic for migrations
- **Docker Compose** for easier development

## Development

The only dependencies for this project should be Python3.11+, docker and docker compose.

### Quick Start

- Starting the project with hot-reloading enabled
(_the first time it will take a while_):

- ```docker compose up -d```
- And navigate to http://localhost:8000
- Auto-generated docs will be at http://localhost:8000/docs

### Rebuilding containers

```bash
docker compose build
```
### Restarting containers

```bash
docker compose restart
```

### Bringing containers down

```bash
docker compose down
```

## Migrations

To create a new migration:

```bash
alembic revision -m "create users table"
```

And fill in `upgrade` and `downgrade` methods. For more information see
[Alembic's official documentation](https://alembic.sqlalchemy.org/en/latest/tutorial.html#create-a-migration-script).

## Logging
```
docker compose logs
```
## Project Layout
```

app
    ├── api
    │   └── api_v1
    │   │    └── endpoints folder
    │   └── dependencies # endpoint dependencies
    ├── config    # config
    ├── crud      # crud methods
    ├── db        # db session and base
    ├── models    # db models
    ├── schemas   # pydantic schemas
    └── main.py # entrypoint to backend
    │ 
migration
    └── versions # where migrations are located
    │ 
scripts # to format code and check lint issues
```
## Repo maintainers

- [Adarsh K R](emailto:adakr@deloitte.com)
- [Nikhil Akki](emailto:niakki@deloitte.com)