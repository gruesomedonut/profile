from typing import Dict

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.crud.users import users as CRUDUsers
from app.schemas.users import UsersBase, UsersEdit


class ExceptionCustom(HTTPException):
    pass


class UserApi:
    @staticmethod
    def create_user(session: Session, user: UsersBase) -> int:
        return CRUDUsers.create(session, obj_in=user).id

    @staticmethod
    def get_user_by_name(session: Session, *, username: str) -> Dict:
        user = CRUDUsers.get_user(session, username=username)

        if not user:
            raise ExceptionCustom(status_code=404, detail="User not found")

        return user.to_dict()

    @staticmethod
    def get_user_by_id(session: Session, *, id: int) -> Dict | None:
        user = CRUDUsers.get(session, id)
        if not user:
            raise ExceptionCustom(status_code=404, detail="User not found")
        return user.to_dict()

    @staticmethod
    def update_user(session: Session, *, id: int, user: UsersEdit) -> None:
        db_obj = CRUDUsers.get(session, id)
        if not db_obj:
            raise ExceptionCustom(status_code=404, detail="User not found")

        CRUDUsers.update(session, db_obj=db_obj, obj_in=user)

    @staticmethod
    def delete_user(session: Session, *, id: int) -> None:
        db_obj = CRUDUsers.get(session, id)
        if not db_obj:
            raise ExceptionCustom(status_code=404, detail="User not found")
        CRUDUsers.remove(session, id=id)
