from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from app.models.users import Users


class Todo(Base):
    title: Mapped[str]
    content: Mapped[str]
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now
    )

    UniqueConstraint("created_by", "title", name="todo_title_created_by_key"),

    user: Mapped["Users"] = relationship()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "user": self.user.to_dict(),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
