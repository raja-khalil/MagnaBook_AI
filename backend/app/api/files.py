from app.api.crud_router import create_crud_router
from app.models.project import File
from app.schemas.file import FileCreate, FileRead, FileUpdate
from app.services.crud import CRUDService

file_service = CRUDService(File)

router = create_crud_router(
    prefix="/files",
    tags=["files"],
    service=file_service,
    create_schema=FileCreate,
    update_schema=FileUpdate,
    read_schema=FileRead,
    not_found_message="File not found",
)
