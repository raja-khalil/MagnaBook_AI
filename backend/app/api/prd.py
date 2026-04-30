from app.api.crud_router import create_crud_router
from app.models.content import PRDVersion
from app.schemas.prd import PRDCreate, PRDRead, PRDUpdate
from app.services.crud import CRUDService

prd_service = CRUDService(PRDVersion)

router = create_crud_router(
    prefix="/prd",
    tags=["prd"],
    service=prd_service,
    create_schema=PRDCreate,
    update_schema=PRDUpdate,
    read_schema=PRDRead,
    not_found_message="PRD not found",
)
