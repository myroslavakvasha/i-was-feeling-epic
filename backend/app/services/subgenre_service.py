from app.repositories import subgenre_repository
from app.schemas.subgenre import SubgenreResponse
from sqlalchemy.orm import Session

def get_all(db: Session) -> list[SubgenreResponse]:
    return [SubgenreResponse.model_validate(s) for s in subgenre_repository.get_all(db)]