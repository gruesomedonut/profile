from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base


class Users(Base):
    username: Mapped[str] = mapped_column(unique=True)
    email_id: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "email_id": self.email_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
