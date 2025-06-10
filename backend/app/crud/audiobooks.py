from typing import List, Optional
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase  # Alterado
from app.models.audiobook import Audiobook  # Alterado
from app.schemas.audiobook import AudiobookCreate, AudiobookUpdate  # Alterado

class CRUDAudiobook(CRUDBase[Audiobook, AudiobookCreate, AudiobookUpdate]):
    def get_multi_by_user(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Audiobook]:
        return (
            db.query(self.model)
            .filter(Audiobook.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, db: Session, *, obj_in: AudiobookCreate) -> Audiobook:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_status(
        self,
        db: Session,
        *,
        db_obj: Audiobook,
        status: str,
        progress: Optional[float] = None,
        current_step: Optional[int] = None,
        error: Optional[str] = None
    ) -> Audiobook:
        if status:
            db_obj.status = status
        if progress is not None:
            db_obj.progress = progress
        if current_step is not None:
            db_obj.current_step = current_step
        if error is not None:
            db_obj.error = error
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

audiobooks = CRUDAudiobook(Audiobook)