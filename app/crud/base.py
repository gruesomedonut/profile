from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, session: Session, id: int) -> Optional[ModelType]:
        return session.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self, session: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return session.query(self.model).offset(skip).limit(limit).all()

    def create(self, session: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        session.flush()
        session.refresh(db_obj)
        return db_obj

    def update(
        self,
        session: Session,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | Dict[str, Any]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        session.add(db_obj)
        session.flush()
        session.refresh(db_obj)
        return db_obj

    def remove(self, session: Session, *, id: int) -> Optional[ModelType]:
        obj = session.query(self.model).get(id)
        session.delete(obj)
        session.flush()
        return obj
