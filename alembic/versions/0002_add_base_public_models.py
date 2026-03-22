"""Add base/public/create/update slices and audit columns.

Revision ID: 0002_add_base_public_models
Revises: 0001_initial
Create Date: 2026-03-22
"""
from __future__ import annotations

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "0002_add_base_public_models"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def _utc_now():
    return sa.text("timezone('utc', now())")


def upgrade() -> None:
    # student
    op.add_column(
        "student",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=_utc_now(),
            nullable=False,
        ),
    )
    op.add_column(
        "student",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=_utc_now(),
            nullable=False,
        ),
    )
    op.drop_column("student", "registered_at")

    # project
    op.add_column(
        "project",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=_utc_now(),
            nullable=False,
        ),
    )

    # projectmember
    op.add_column(
        "projectmember",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=_utc_now(),
            nullable=False,
        ),
    )
    op.add_column(
        "projectmember",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=_utc_now(),
            nullable=False,
        ),
    )

    # team
    op.add_column(
        "team",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=_utc_now(),
            nullable=False,
        ),
    )
    op.add_column(
        "team",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=_utc_now(),
            nullable=False,
        ),
    )

    # sprint
    op.add_column(
        "sprint",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=_utc_now(),
            nullable=False,
        ),
    )

    # teammembership
    op.add_column(
        "teammembership",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=_utc_now(),
            nullable=False,
        ),
    )
    op.add_column(
        "teammembership",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=_utc_now(),
            nullable=False,
        ),
    )

    # sprinttask
    op.add_column(
        "sprinttask",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=_utc_now(),
            nullable=False,
        ),
    )

    # taskassignment
    op.add_column(
        "taskassignment",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=_utc_now(),
            nullable=False,
        ),
    )
    op.add_column(
        "taskassignment",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=_utc_now(),
            nullable=False,
        ),
    )
    op.alter_column("taskassignment", "assignet_at", new_column_name="assigned_at")

    # taskchangerequest
    op.add_column(
        "taskchangerequest",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=_utc_now(),
            nullable=False,
        ),
    )

    # busyslot
    op.add_column(
        "busyslot",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=_utc_now(),
            nullable=False,
        ),
    )


def downgrade() -> None:
    # busyslot
    op.drop_column("busyslot", "updated_at")

    # taskchangerequest
    op.drop_column("taskchangerequest", "updated_at")

    # taskassignment
    op.alter_column("taskassignment", "assigned_at", new_column_name="assignet_at")
    op.drop_column("taskassignment", "updated_at")
    op.drop_column("taskassignment", "created_at")

    # sprinttask
    op.drop_column("sprinttask", "updated_at")

    # teammembership
    op.drop_column("teammembership", "updated_at")
    op.drop_column("teammembership", "created_at")

    # sprint
    op.drop_column("sprint", "updated_at")

    # team
    op.drop_column("team", "updated_at")
    op.drop_column("team", "created_at")

    # projectmember
    op.drop_column("projectmember", "updated_at")
    op.drop_column("projectmember", "created_at")

    # project
    op.drop_column("project", "updated_at")

    # student
    op.add_column(
        "student",
        sa.Column(
            "registered_at",
            sa.DateTime(timezone=True),
            server_default=_utc_now(),
            nullable=False,
        ),
    )
    op.drop_column("student", "updated_at")
    op.drop_column("student", "created_at")
