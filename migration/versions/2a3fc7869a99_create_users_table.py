"""create users table

Revision ID: 2a3fc7869a99
Revises:
Create Date: 2023-04-11 16:04:47.030853

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "2a3fc7869a99"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("username", sa.String(), unique=True, nullable=False),
        sa.Column("email_id", sa.String(), unique=True, nullable=False),
        sa.Column("created_at", sa.DateTime()),
        sa.Column("updated_at", sa.DateTime()),
    )
    op.create_index("users_idx", "users", ["id", "username"])


def downgrade():
    op.drop_index("users_idx", "users")
    op.drop_table("users")
