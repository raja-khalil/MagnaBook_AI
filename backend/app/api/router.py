from fastapi import APIRouter

from app.api.book import router as book_router
from app.api.briefing import router as briefing_router
from app.api.export import router as export_router
from app.api.files import router as files_router
from app.api.health import router as health_router
from app.api.prd import router as prd_router
from app.api.projects import router as projects_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(projects_router)
api_router.include_router(files_router)
api_router.include_router(briefing_router)
api_router.include_router(prd_router)
api_router.include_router(book_router)
api_router.include_router(export_router)
