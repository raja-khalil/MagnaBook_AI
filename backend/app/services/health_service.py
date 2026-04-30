from app.schemas.health import HealthResponse


def get_health_status() -> HealthResponse:
    return HealthResponse(
        status="ok",
        service="magnabook-ai-api",
        version="0.1.0",
    )
