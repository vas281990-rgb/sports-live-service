from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def healthcheck():
    # Lightweight endpoint for container and monitoring checks.
    return {"status": "ok"}