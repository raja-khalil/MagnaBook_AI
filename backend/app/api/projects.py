from app.api.crud_router import create_crud_router
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectRead, ProjectUpdate
from app.services.crud import CRUDService

project_service = CRUDService(Project)

router = create_crud_router(
    prefix="/projects",
    tags=["projects"],
    service=project_service,
    create_schema=ProjectCreate,
    update_schema=ProjectUpdate,
    read_schema=ProjectRead,
    not_found_message="Project not found",
)
