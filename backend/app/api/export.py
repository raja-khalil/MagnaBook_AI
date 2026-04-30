from app.api.crud_router import create_crud_router
from app.models.export import Export
from app.schemas.export import ExportCreate, ExportRead, ExportUpdate
from app.services.crud import CRUDService

export_service = CRUDService(Export)

router = create_crud_router(
    prefix="/export",
    tags=["export"],
    service=export_service,
    create_schema=ExportCreate,
    update_schema=ExportUpdate,
    read_schema=ExportRead,
    not_found_message="Export not found",
)
