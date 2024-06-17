from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.users import Users
from app.schemas.users import UsersBase, UsersEdit


class CRUDUsers(CRUDBase[Users, UsersBase, UsersEdit]):
    def get_user(
        self, session: Session, *, username: str, email_id: str = ""
    ) -> Users | None:
        query = session.query(Users).filter(Users.username == username)

        if email_id:
            query = query.filter(Users.email_id == email_id)

        user = query.first()

        if not user:
            return None

        return user


users = CRUDUsers(Users)
