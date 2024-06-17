from datetime import datetime

from pydantic import BaseModel, EmailStr


class UsersBase(BaseModel):
    username: str
    email_id: EmailStr


class UsersCreateResponse(BaseModel):
    id: int


class UsersResponse(UsersBase):
    id: int
    created_at: datetime
    updated_at: datetime


class UsersEdit(BaseModel):
    username: str
    email_id: EmailStr
