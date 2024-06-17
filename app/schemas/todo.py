from datetime import datetime

from pydantic import BaseModel

from app.schemas.users import UsersResponse


class TodoBase(BaseModel):
    title: str
    content: str
    created_by: int


class TodoBaseEdit(BaseModel):
    title: str
    content: str
    created_by: int


class TodoCreateResponse(BaseModel):
    id: int


class TodoResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    user: UsersResponse
