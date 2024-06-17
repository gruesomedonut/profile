from fastapi import APIRouter

from app.api.api_v1.status.route import status_router
from app.api.api_v1.todo.route import todo_router
from app.api.api_v1.users.route import user_router

api_router = APIRouter()
api_router.include_router(status_router)
api_router.include_router(user_router)
api_router.include_router(todo_router)
