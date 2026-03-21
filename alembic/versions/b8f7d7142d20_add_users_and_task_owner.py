"""add users and task owner

Revision ID: b8f7d7142d20
Revises: 417c51580d8c
Create Date: 2026-03-21 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b8f7d7142d20"
down_revision: Union[str, Sequence[str], None] = "417c51580d8c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=50), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_index(op.f("ix_users_username"), "users", ["username"], unique=True)

    op.execute(
        sa.text(
            """
            INSERT INTO users (username, hashed_password)
            VALUES ('system', '$2b$12$0JFTI5hWdc7CWQ6dJXHTr.g8s03tw5W5x6WvFdu8fNJfgK4fVCYfy')
            ON CONFLICT (username) DO NOTHING
            """
        )
    )

    op.add_column("tasks", sa.Column("owner_id", sa.Integer(), nullable=True))
    op.create_index(op.f("ix_tasks_owner_id"), "tasks", ["owner_id"], unique=False)
    op.create_foreign_key(
        "fk_tasks_owner_id_users",
        "tasks",
        "users",
        ["owner_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.execute(sa.text("UPDATE tasks SET owner_id = 1 WHERE owner_id IS NULL"))
    op.alter_column("tasks", "owner_id", nullable=False)


def downgrade() -> None:
    op.drop_constraint("fk_tasks_owner_id_users", "tasks", type_="foreignkey")
    op.drop_index(op.f("ix_tasks_owner_id"), table_name="tasks")
    op.drop_column("tasks", "owner_id")

    op.drop_index(op.f("ix_users_username"), table_name="users")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_table("users")
