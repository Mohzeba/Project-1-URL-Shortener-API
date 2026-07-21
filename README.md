# Project-1-URL-Shortener-API

# URL Shortener + Analytics API

A backend API that shortens URLs and tracks click analytics, built with FastAPI, PostgreSQL, Redis, and Docker.

## Features
- Shorten a long URL into a short code (random or custom)
- Redirect via short code, with click tracking
- Redis caching for fast repeat redirects (falls back to PostgreSQL on cache miss)
- View click analytics per short code
- List all shortened URLs
- Delete a shortened URL

## Tech Stack
- **FastAPI** — API framework
- **PostgreSQL** — persistent storage
- **Redis** — caching layer for hot short codes
- **Docker / Docker Compose** — containerized local development

## Running locally

```bash
git clone <your-repo-url>
cd url-shortener-api
docker compose up --build
```

API available at `http://localhost:8000`
Interactive docs at `http://localhost:8000/docs`

## Endpoints

| Method | Path | Description |
|---|---|---|
| POST | `/shorten` | Create a short URL (optional custom code) |
| GET | `/{short_code}` | Get the long URL for a short code (tracks click, checks Redis cache first) |
| GET | `/{short_code}/stats` | View click analytics for a short code |
| GET | `/urls` | List all shortened URLs |
| DELETE | `/{short_code}` | Delete a shortened URL |

## Project Structure

```
url-shortener-api/
├── app/
│   ├── main.py         # FastAPI app entry point
│   ├── models.py        # Database table schema
│   ├── database.py      # DB connection setup
│   └── routes.py         # API endpoints
├── docker-compose.yml    # App + Postgres + Redis containers
├── Dockerfile             # App container build instructions
├── requirements.txt
└── .env
```