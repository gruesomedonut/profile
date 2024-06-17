from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.todo import Todo
from app.schemas.todo import TodoBase, TodoBaseEdit


class CRUDTodo(CRUDBase[Todo, TodoBase, TodoBaseEdit]):
    def get_todos(self, db: Session, *, created_by: int) -> list[Todo]:
        return db.query(self.model).filter(Todo.created_by == created_by).all()

    def delete(self, db: Session, *, id: int) -> None:
        db.query(self.model).filter(Todo.id == id).delete()


todo = CRUDTodo(Todo)
