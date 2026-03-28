# Staxa Demo — FastAPI + PostgreSQL

A fullstack contact manager application built with **FastAPI** and **PostgreSQL**. This is a demo/starter template designed for deployment on the [Staxa](https://staxa.dev) PaaS platform.

## Tech Stack

- **Framework**: FastAPI (Python 3.12)
- **Database**: PostgreSQL 16
- **ORM**: SQLAlchemy 2.0
- **Templates**: Jinja2
- **Server**: Uvicorn

## Features

- Full CRUD for contacts (name, email, phone, notes)
- Server-rendered HTML views with Jinja2 templates
- JSON API endpoints at `/api/contacts`
- Health check at `/healthz` with database connectivity verification
- Auto-migration and seed data on first startup

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | Yes | `postgresql://postgres:postgres@localhost:5432/fastapi_postgres` | PostgreSQL connection string |
| `PORT` | No | `8000` | Server port (used in Docker CMD) |

## Local Development

```bash
# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up a local PostgreSQL database
createdb fastapi_postgres

# Run the app
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/fastapi_postgres" \
  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open http://localhost:8000 to see the contact manager.

## Docker

```bash
# Build the image
docker build -t staxa-demo-fastapi-postgres .

# Run (assumes local PostgreSQL is accessible)
docker run \
  -e DATABASE_URL="postgresql://postgres:postgres@host.docker.internal:5432/fastapi_postgres" \
  -p 8000:8000 \
  staxa-demo-fastapi-postgres
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/contacts` | List all contacts |
| `POST` | `/api/contacts` | Create a contact |
| `GET` | `/api/contacts/:id` | Get one contact |
| `PUT` | `/api/contacts/:id` | Update a contact |
| `DELETE` | `/api/contacts/:id` | Delete a contact |
| `GET` | `/healthz` | Health check |

## Deployment on Staxa

This app is designed for deployment on Staxa. Push to GitHub and create a tenant using the FastAPI + PostgreSQL template. The `DATABASE_URL` environment variable is automatically injected at runtime.
