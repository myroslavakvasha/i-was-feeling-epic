from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.subgenre import SubgenreResponse
from app.deps import get_db
from app.services import subgenre_service

router = APIRouter(prefix="/subgenres", tags=["subgenres"]) # tag is what's shown in swagger

@router.get("", response_model=list[SubgenreResponse])
def get_all(db: Session = Depends(get_db)):
    return subgenre_service.get_all(db)