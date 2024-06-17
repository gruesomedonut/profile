import logging

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.api_key import APIKey
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError

from app.api.api_v1.users.controller import ExceptionCustom, UserApi
from app.api.dependencies import deps
from app.db.session import acquire_db_session
from app.schemas.users import UsersBase, UsersCreateResponse, UsersEdit, UsersResponse

logger = logging.getLogger(__name__)


user_router = APIRouter(
    prefix="/user",
    tags=["Users"],
)


@user_router.get("/{username}", response_model=UsersResponse)
def get_user(username: str, _: APIKey = Depends(deps.get_api_key)) -> UsersResponse:
    try:
        with acquire_db_session() as session:
            user = UserApi.get_user_by_name(session, username=username)

        return UsersResponse(**user)
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
            detail="Issues in user get enpoint",
        ) from e


@user_router.post("", response_model=UsersCreateResponse)
def create_user(
    user: UsersBase, _: APIKey = Depends(deps.get_api_key)
) -> UsersCreateResponse | None:
    try:
        with acquire_db_session() as session:
            user_id: int = UserApi.create_user(session, user)

        return UsersCreateResponse(id=user_id)
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
            detail="Issues in user create enpoint",
        ) from e


@user_router.put("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update_user(
    id: int, user: UsersEdit, _: APIKey = Depends(deps.get_api_key)
) -> None:
    try:
        with acquire_db_session() as session:
            UserApi.update_user(session, id=id, user=user)

    except ExceptionCustom as e:
        logger.error(str(e))
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail,
        ) from e
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
            detail="Issues in user update enpoint",
        ) from e


@user_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, _: APIKey = Depends(deps.get_api_key)) -> None:
    try:
        with acquire_db_session() as session:
            UserApi.delete_user(
                session,
                id=id,
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
            detail="Issues in user delete enpoint",
        ) from e
