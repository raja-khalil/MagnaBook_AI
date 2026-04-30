from app.api.crud_router import create_crud_router
from app.models.content import BookVersion
from app.schemas.book import BookCreate, BookRead, BookUpdate
from app.services.crud import CRUDService

book_service = CRUDService(BookVersion)

router = create_crud_router(
    prefix="/book",
    tags=["book"],
    service=book_service,
    create_schema=BookCreate,
    update_schema=BookUpdate,
    read_schema=BookRead,
    not_found_message="Book version not found",
)
