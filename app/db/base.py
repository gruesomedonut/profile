# Import all the models, so that Base has them before being
# imported by Alembic

from app.db.base_class import Base  # noqa
from app.models.users import Users  # noqa
from app.models.todo import Todo  # noqa
