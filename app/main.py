from fastapi import FastAPI
# Import individual routing modules for different API features
from app.api.routes.health import router as health_router
from app.api.routes.ingestion import router as ingestion_router
from app.api.routes.live import router as live_router
from app.api.routes.monitoring import router as monitoring_router

# FIX: import tasks here so Celery discovers them without circular imports.
import app.workers.tasks  # noqa: F401

# Initialize the FastAPI app with metadata for documentation
app = FastAPI(
    title="Sports Live Service",
    version="1.0.0",
    description="Mini-service for live football ingestion and normalized hot-path API.",
)

# Register routers under the /api/v1 prefix and group them with tags
app.include_router(health_router, prefix="/api/v1", tags=["Health"])
app.include_router(ingestion_router, prefix="/api/v1", tags=["Ingestion"])
app.include_router(live_router, prefix="/api/v1", tags=["Live Events"])
app.include_router(monitoring_router, prefix="/api/v1", tags=["Monitoring"])