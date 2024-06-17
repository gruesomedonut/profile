"""create todo table

Revision ID: 5a5e4b6f3adc
Revises: 2a3fc7869a99
Create Date: 2023-04-11 16:06:08.306433

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '5a5e4b6f3adc'
down_revision = '2a3fc7869a99'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "todo",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("content", sa.String()),
        sa.Column(
            "created_by",
            sa.Integer,
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime()),
        sa.Column("updated_at", sa.DateTime()),
    )

    op.create_unique_constraint(
        "todo_title_created_by_key", "todo", ["created_by", "title"]
    )
    op.create_index("todo_idx", "todo", ["id", "title"])


def downgrade():
    op.drop_constraint("todo_title_created_by_key", "todo")
    op.drop_index("todo_idx", "todo")
    op.drop_table("todo")
