"""add_hashed_password_to_student

Revision ID: 08185b82777d
Revises: 0002_add_base_public_models
Create Date: 2026-04-28 17:37:16.949012
"""

from __future__ import annotations

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '08185b82777d'
down_revision = '0002_add_base_public_models'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'student', sa.Column('hashed_password', sa.String(255), nullable=True)
    )


def downgrade() -> None:
    op.drop_column('student', 'hashed_password')
