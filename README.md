
# Sports Live Service

Mini-service for live football events.

The service follows the required architecture:

```text
fixture JSON live-events
        ↓
raw snapshots
        ↓
normalization worker
        ↓
normalized PostgreSQL tables
        ↓
FastAPI response close to upstream format


⸻


Stack
FastAPI
PostgreSQL
Redis
Celery
SQLAlchemy
Alembic
Pytest


⸻


Architecture Overview
Ingestion Flow
Fixture JSON is loaded through ingestion endpoint.
Raw upstream payload is stored in raw_snapshots.
Celery worker normalizes payload into relational tables:
teams
tournaments
events
scores
Live endpoint reads only normalized PostgreSQL tables.
Hot path never reads raw JSON directly.


⸻


Requirements Covered
Requirement
Status
Fixture JSON live-events
✅
Store raw snapshot
✅
Normalize events/teams/tournaments/scores
✅
GET /api/v1/sport/football/events/live
✅
Hot path reads normalized tables only
✅
Exclude isEditor=true hard-ban events
✅
Swagger
✅
Migrations/schema
✅
Tests
✅
Benchmark p50/p95
✅
Retries/backoff
✅
Backfill checkpointing description/code
✅
Monitoring live freshness
✅
Raw snapshots as replay/fallback
✅


⸻


Project Structure
sports-live-service/
│
├── alembic/
├── app/
│   ├── api/
│   │   └── routes/
│   ├── core/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── workers/
│
├── fixture/
├── scripts/
├── tests/
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── alembic.ini
├── pytest.ini
└── README.md


⸻


Run Project
Create environment file:
cp .env.example .env
Start services:
docker compose up --build


⸻


Run Migrations
Inside API container:
docker compose exec api alembic upgrade head


⸻


Swagger
http://localhost:8000/docs


⸻


Ingest Fixture
curl -X POST http://localhost:8000/api/v1/sport/football/ingest-fixture
Expected response:
{
  "status": "accepted",
  "snapshot_id": 1,
  "message": "Raw snapshot stored and normalization task scheduled."
}


⸻


Live Endpoint
curl http://localhost:8000/api/v1/sport/football/events/live
Endpoint:
reads normalized tables only;
does not access raw JSON in hot path;
excludes isEditor=true hard-ban events;
returns SofaScore-like response shape.


⸻


Monitoring Endpoint
curl http://localhost:8000/api/v1/monitoring/live-freshness
Endpoint calculates freshness using:
now() - max(events.upstream_updated_at)
Suggested thresholds:
Level
Condition
OK
freshness <= 10 sec
Warning
freshness > 10 sec
Critical
freshness > 30 sec
Target live freshness is around 5 seconds.


⸻


Benchmark
Run benchmark:
docker compose exec api python scripts/benchmark_live_endpoint.py
Example result:
Requests: 100
P50 latency: 11.91 ms
P95 latency: 18.88 ms


⸻


Run Tests
docker compose exec api pytest
Example result:
7 passed


⸻


Retries and Backoff
Celery normalization task uses automatic retries with exponential backoff and jitter:
autoretry_for=(Exception,)
retry_backoff=True
retry_jitter=True
max_retries=5
This protects ingestion and normalization pipeline from temporary:
PostgreSQL failures;
Redis connection issues;
worker/network interruptions.


⸻


Backfill Checkpointing
For historical backfill, service stores checkpoint cursor in:
backfill_checkpoints
Suggested flow:
read checkpoint
fetch history page
store raw snapshot
normalize snapshot
save checkpoint
repeat
This allows safe resume after:
worker restart;
deployment interruption;
temporary upstream failure.


⸻


Raw Snapshots as Replay/Fallback
Original upstream payloads are stored in:
raw_snapshots.payload
They can be used for:
replaying normalization;
rebuilding normalized tables;
debugging upstream payload changes;
recovery after normalization failures;
audit/debug purposes.


⸻


PostgreSQL Hot Path Optimization
Live endpoint queries only normalized relational tables:
events
teams
tournaments
scores
Benefits:
lower response latency;
indexed SQL access;
no JSON parsing in hot path;
easier scaling and caching.


⸻


Production Improvements
For production version I would additionally add:
Prometheus/Grafana metrics;
structured JSON logging;
dead-letter queue for failed tasks;
periodic polling scheduler;
upstream API rate limiting;


OpenTelemetry tracing;
read replicas for hot-path scaling;
load testing with large live event volume;
partitioning for historical snapshots;
Redis caching layer for ultra-hot endpoints.


⸻