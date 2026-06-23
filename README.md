# PipelineIQ

## Overview

PipelineIQ is a CI/CD observability and incident analysis platform built for automated pipeline failure detection, root cause classification, remediation guidance, alerting, and visualization.

The project uses a Python FastAPI backend with SQLite persistence, a React + Vite dashboard, Slack notifications, Prometheus metrics, and Docker Compose orchestration.

## Key Features

- Automated ingestion of CI/CD failure logs
- Rule-based AI failure analysis and categorization
- Root cause identification, remediation suggestion, and confidence scoring
- Slack alerting for pipeline incidents
- Historical pipeline run storage and dashboard visualization
- Prometheus-compatible metrics endpoint
- Dockerized backend, frontend, and monitoring stack

## Architecture

```
GitHub Actions / Azure Pipelines
                |
                v
         PipelineIQ API (FastAPI)
                |
                v
   Failure analysis / Slack alerting
                |
      -----------------------------
      |                           |
      v                           v
   SQLite                    Prometheus
   pipelineiq.db              metrics endpoint
                |
                v
        React Dashboard
```

## Technology Stack

### Backend

- FastAPI
- Python
- SQLAlchemy
- SQLite
- Pydantic
- Uvicorn
- prometheus-client

### Frontend

- React
- Vite
- Axios
- Chart.js
- React ChartJS 2

### Infrastructure

- Docker
- Docker Compose
- Prometheus
- Grafana
- GitHub Actions

## Repository Structure

```
pipelineiq/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── database.py
│   │   └── config.py
│   ├── routes/
│   │   ├── health.py
│   │   ├── pipeline.py
│   │   └── metrics.py
│   ├── services/
│   │   ├── ai_service.py
│   │   ├── github_service.py
│   │   ├── azure_service.py
│   │   ├── notification_service.py
│   │   └── slack_service.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   ├── App.css
│   │   └── index.css
│   ├── package.json
│   ├── Dockerfile
│   └── README.md
├── monitoring/
│   └── prometheus.yml
├── .github/
│   └── workflows/pipelineiq.yml
├── docker-compose.yml
└── README.md
```

## Backend API Endpoints

### Health Check

`GET /health`

Response:

```json
{
  "status": "healthy",
  "service": "PipelineIQ"
}
```

### Analyze Failure

`POST /analyze-failure`

Request body:

```json
{
  "run_id": "github-actions",
  "failure_log": "ModuleNotFoundError: No module named pandas123",
  "commit_sha": "abcdef123456"
}
```

Behavior:

- classifies the failure log
- stores a `PipelineRun` record in SQLite
- increments Prometheus counters
- sends a Slack alert

### Pipeline Runs

`GET /pipeline-runs`

Returns all stored pipeline run records.

### Dashboard Statistics

`GET /stats`

Response example:

```json
{
  "total_runs": 10,
  "failed_runs": 7,
  "success_rate": 30.0
}
```

### Prometheus Metrics

`GET /metrics`

Exposes Prometheus metrics such as:

- `pipeline_runs_total`
- `pipeline_failures_total`

## Failure Analysis Engine

The backend analyzes failure logs using `backend/services/ai_service.py` and returns:

- `category`
- `root_cause`
- `fix`
- `confidence`

Supported classification categories include:

- Dependency Error
- Test Failure
- Database Error
- Docker Error
- Permission Error
- CI/CD Failure
- Unknown Error

## Data Model

The `PipelineRun` model in `backend/app/models.py` includes:

- `id`
- `run_id`
- `status`
- `failure_log`
- `category`
- `confidence`
- `ai_suggestion`
- `commit_sha`
- `created_at`

## Frontend Dashboard

The React dashboard in `frontend/src/App.jsx` displays:

- total runs
- failed runs
- success rate
- top failure category
- failure category distribution pie chart
- pipeline runs table
- selected run details, including failure log and AI suggestion

The UI fetches data from the backend at:

- `http://127.0.0.1:8000/stats`
- `http://127.0.0.1:8000/pipeline-runs`

## CI/CD Integration

### GitHub Actions

A sample GitHub Actions workflow is available in `.github/workflows/pipelineiq.yml`.
It simulates a failure, captures the failed step outcome, and sends the failure log to the PipelineIQ API for analysis.

### Azure DevOps Pipeline

A sample Azure DevOps pipeline is defined in `azure-pipelines.yml`.
This pipeline installs dependencies, simulates a failure condition, and is structured to provide a repeatable Azure-based CI/CD integration path for PipelineIQ.

## Docker Deployment

Start the full stack:

```bash
docker compose up --build
```

Stop services:

```bash
docker compose down
```

Services defined in `docker-compose.yml`:

- `backend`
- `frontend`
- `prometheus`
- `grafana`

## Local Development

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend URL:

`http://127.0.0.1:8000`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend URL:

`http://localhost:5173`

## Environment Variables

The backend uses environment variables loaded from `backend/.env` when available.

Required:

- `SLACK_WEBHOOK_URL`

Optional:

- `GITHUB_TOKEN`
- `AZURE_ORG`
- `AZURE_PROJECT`
- `AZURE_PAT`
- `OPENAI_API_KEY`

> Note: `backend/app/database.py` currently uses a local SQLite file at `pipelineiq.db`.

## Security

- Keep secrets out of version control.
- Store API keys and credentials in environment variables or secret stores.
- Do not commit `backend/.env`.

## Future Enhancements

- full OpenAI-powered failure analysis
- GitHub commit comment posting
- Azure DevOps pipeline triggering
- Grafana dashboard integration
- real-time alert routing and incident workflows

## Author

Sharmishta T

Dayananda Sagar Academy of Technology and Management

Computer Science and Engineering, 2027 Batch
