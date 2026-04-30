from app.api.crud_router import create_crud_router
from app.models.content import Briefing
from app.schemas.briefing import BriefingCreate, BriefingRead, BriefingUpdate
from app.services.crud import CRUDService

briefing_service = CRUDService(Briefing)

router = create_crud_router(
    prefix="/briefing",
    tags=["briefing"],
    service=briefing_service,
    create_schema=BriefingCreate,
    update_schema=BriefingUpdate,
    read_schema=BriefingRead,
    not_found_message="Briefing not found",
)
