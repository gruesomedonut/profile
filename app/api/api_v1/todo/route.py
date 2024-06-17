import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.api_key import APIKey
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError

from app.api.api_v1.todo.controller import ExceptionCustom, TodoApi
from app.api.dependencies import deps
from app.db.session import acquire_db_session
from app.schemas.todo import TodoBase, TodoBaseEdit, TodoCreateResponse, TodoResponse

logger = logging.getLogger(__name__)


todo_router = APIRouter(
    prefix="/todo",
    tags=["Todo"],
)


@todo_router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(
    todo_id: int, _: APIKey = Depends(deps.get_api_key)
) -> TodoResponse | None:
    try:
        with acquire_db_session() as session:
            todo = TodoApi.get_todo(session, todo_id=todo_id)

        return TodoResponse(**todo)
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Issues in todo get enpoint",
        ) from None


@todo_router.get("", response_model=List[TodoResponse])
def get_todos(_: APIKey = Depends(deps.get_api_key)) -> List[TodoResponse] | None:
    try:
        with acquire_db_session() as session:
            todos = TodoApi.get_todos(session)

        return todos
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Issues in todo get enpoint",
        ) from None


@todo_router.post("/", response_model=TodoCreateResponse)
def create_todo(
    todo: TodoBase, _: APIKey = Depends(deps.get_api_key)
) -> TodoCreateResponse | None:
    try:
        with acquire_db_session() as session:
            todo_id = TodoApi.create_todo(session, todo=todo)

        return TodoCreateResponse(id=todo_id)
    except IntegrityError as e:
        logger.error(str(e))
        if isinstance(e.orig, UniqueViolation):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Duplicate entry",
            ) from e

    except Exception as e:
        logger.error(str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Issues in todo create enpoint",
        ) from e


@todo_router.put("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_todo(
    todo_id: int, todo: TodoBaseEdit, _: APIKey = Depends(deps.get_api_key)
) -> None:
    try:
        with acquire_db_session() as session:
            TodoApi.edit_todo(
                session,
                todo=todo,
                todo_id=todo_id,
            )

    except ExceptionCustom as e:
        logger.error(str(e))
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail,
        ) from e
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Issues in todo update enpoint",
        ) from e


@todo_router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, _: APIKey = Depends(deps.get_api_key)) -> None:
    try:
        with acquire_db_session() as session:
            TodoApi.delete_todo(
                session,
                todo_id=todo_id,
            )

    except ExceptionCustom as e:
        logger.error(str(e))
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail,
        ) from e
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Issues in todo delete enpoint",
        ) from e
