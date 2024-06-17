from typing import Dict, List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.crud.todo import todo as CRUDTodo
from app.schemas.todo import TodoBase, TodoBaseEdit, TodoResponse


class ExceptionCustom(HTTPException):
    pass


class TodoApi:
    @staticmethod
    def get_todo(session: Session, *, todo_id: int) -> Dict:
        todo = CRUDTodo.get(session, todo_id)
        if not todo:
            raise ExceptionCustom(status_code=404, detail="Todo not found")
        return todo.to_dict()

    @staticmethod
    def get_todos(
        session: Session,
    ) -> List[TodoResponse]:
        todos = CRUDTodo.get_multi(session)
        return [TodoResponse(**todo.to_dict()) for todo in todos]

    @staticmethod
    def create_todo(session: Session, *, todo: TodoBase) -> int:
        return CRUDTodo.create(session, obj_in=todo).id

    @staticmethod
    def edit_todo(session: Session, *, todo: TodoBaseEdit, todo_id: int) -> None:
        db_obj = CRUDTodo.get(session, todo_id)

        if not db_obj:
            raise ExceptionCustom(status_code=404, detail="Todo not found")

        CRUDTodo.update(session, db_obj=db_obj, obj_in=todo)

    @staticmethod
    def delete_todo(session: Session, *, todo_id: int) -> None:
        db_obj = CRUDTodo.get(session, todo_id)
        if not db_obj:
            raise ExceptionCustom(status_code=404, detail="Todo not found")
        CRUDTodo.delete(session, id=todo_id)
