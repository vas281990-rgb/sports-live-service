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
```

---

## Stack

- FastAPI
- PostgreSQL
- Redis
- Celery
- SQLAlchemy
- Alembic
- Pytest

---

## Requirements covered

| Requirement | Status |
|---|---|
| Fixture JSON live-events | ✅ |
| Store raw snapshot | ✅ |
| Normalize events/teams/tournaments/scores | ✅ |
| GET `/api/v1/sport/football/events/live` | ✅ |
| Hot path reads normalized tables only | ✅ |
| Filter `isEditor=true` | ✅ |
| Swagger | ✅ |
| Migrations/schema | ✅ |
| Tests | ✅ |
| Benchmark p50/p95 | ✅ |
| Retries/backoff | ✅ |
| Backfill checkpointing description/code | ✅ |
| Monitoring live freshness | ✅ |
| Raw snapshots as replay/fallback | ✅ |

---

## Run project

```bash
cp .env.example .env
docker compose up --build
```

---

## Run migrations

Inside API container:

```bash
docker compose exec api alembic upgrade head
```

---

## Swagger

```text
http://localhost:8000/docs
```

---

## Ingest fixture

```bash
curl -X POST http://localhost:8000/api/v1/sport/football/ingest-fixture
```

---

## Live endpoint

```bash
curl http://localhost:8000/api/v1/sport/football/events/live
```

---

## Benchmark

```bash
python scripts/benchmark_live_endpoint.py
```

---

## Run tests

```bash
pytest
```