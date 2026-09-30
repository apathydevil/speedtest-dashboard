# speedtest-dashboard

A small FastAPI web app that displays results from a self-hosted
[Speedtest Tracker](https://github.com/alexjustesen/speedtest-tracker) instance
through its REST API. It gives a read-only overview of connection speeds
without having to log in to Speedtest Tracker itself.

Built for my homelab, where it runs as a Docker container next to Speedtest Tracker.

## Features

- Latest result: download, upload, ping, and time taken per test phase
- Statistics across all results: average, minimum, and maximum download, upload, and ping
- History of the 10 most recent results, including a count of failed tests
- Button to trigger a new speedtest on demand; the page refreshes automatically
  while the test is running

## Stack

- **FastAPI** — serves the dashboard as server-rendered HTML pages with basic CSS
- **requests** — client for the Speedtest Tracker API (bearer token authentication)
- **python-dotenv** — reads configuration from a `.env` file
- **Docker** — container image based on `python:3.13-slim`

## Configuration

The app needs the URL of a Speedtest Tracker instance and an API token created
in Speedtest Tracker. Copy `.env.example` to `.env` and fill in both values:

```
SPEEDTEST_URL=http://your-speedtest-tracker:port
SPEEDTEST_TOKEN=your-api-token
```

## Run locally

```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
uvicorn main:app --reload
```

The dashboard is available at `http://127.0.0.1:8000`.

## Run with Docker

```bash
docker build -t speedtest-dashboard .
docker run -d --env-file .env -p 8000:8000 speedtest-dashboard
```

## Endpoints

| Method | Path   | Description                                  |
| ------ | ------ | -------------------------------------------- |
| GET    | `/`    | Dashboard with latest result, stats, history |
| POST   | `/run` | Queue a new speedtest                        |

## Possible improvements

- Move the HTML out of Python strings into templates (e.g. Jinja2)
- Replace `print` error output with proper logging and set request timeouts
- Add tests with a mocked Speedtest Tracker API
