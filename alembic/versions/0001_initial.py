"""Initial schema

Revision ID: 0001_initial
Revises: 
Create Date: 2026-03-22
"""
from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    statustype = sa.Enum(
        "open",
        "in_progress",
        "review",
        "testing",
        "done",
        name="statustype",
    )
    taskpriority = sa.Enum(
        "LOW",
        "MEDIUM",
        "HIGH",
        "CRITICAL",
        name="taskpriority",
    )
    taskchangerequeststatus = sa.Enum(
        "pending",
        "approved",
        "rejected",
        name="taskchangerequeststatus",
    )
    slottype = sa.Enum("pair", "credit", "exam", "personal", name="slottype")

    statustype.create(op.get_bind(), checkfirst=True)
    taskpriority.create(op.get_bind(), checkfirst=True)
    taskchangerequeststatus.create(op.get_bind(), checkfirst=True)
    slottype.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "student",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("first_name", sa.String(length=100), nullable=False),
        sa.Column("last_name", sa.String(length=100), nullable=False),
        sa.Column("registered_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("skills", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_student_email"), "student", ["email"], unique=False)

    op.create_table(
        "project",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("owner_student_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(["owner_student_id"], ["student.id"],),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "projectmember",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("role", sa.String(length=50), nullable=False),
        sa.Column("join_date", sa.Date(), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.ForeignKeyConstraint(["project_id"], ["project.id"],),
        sa.ForeignKeyConstraint(["student_id"], ["student.id"],),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "team",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["project_id"], ["project.id"],),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "sprint",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["project_id"], ["project.id"],),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "teammembership",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("team_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("project_member_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("position", sa.String(length=100), nullable=False),
        sa.ForeignKeyConstraint(["project_member_id"], ["projectmember.id"],),
        sa.ForeignKeyConstraint(["team_id"], ["team.id"],),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "sprinttask",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("sprint_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", statustype, server_default="open", nullable=False),
        sa.Column("priority", taskpriority, server_default="LOW", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["project_id"], ["project.id"],),
        sa.ForeignKeyConstraint(["sprint_id"], ["sprint.id"],),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "taskassignment",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("project_task_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("project_member_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("assignet_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("accepted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["project_member_id"], ["projectmember.id"],),
        sa.ForeignKeyConstraint(["project_task_id"], ["sprinttask.id"],),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "taskchangerequest",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("task_assignment_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("requested_by_member_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("status", taskchangerequeststatus, server_default="pending", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("handled_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["requested_by_member_id"], ["projectmember.id"],),
        sa.ForeignKeyConstraint(["task_assignment_id"], ["taskassignment.id"],),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "busyslot",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("slot_type", slottype, nullable=False),
        sa.Column("start_datetime", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_datetime", sa.DateTime(timezone=True), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("source", sa.String(length=50), nullable=False),
        sa.Column("task_assignment_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(["student_id"], ["student.id"],),
        sa.ForeignKeyConstraint(["task_assignment_id"], ["taskassignment.id"],),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("busyslot")
    op.drop_table("taskchangerequest")
    op.drop_table("taskassignment")
    op.drop_table("sprinttask")
    op.drop_table("teammembership")
    op.drop_table("sprint")
    op.drop_table("team")
    op.drop_table("projectmember")
    op.drop_table("project")
    op.drop_index(op.f("ix_student_email"), table_name="student")
    op.drop_table("student")

    sa.Enum(name="slottype").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="taskchangerequeststatus").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="taskpriority").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="statustype").drop(op.get_bind(), checkfirst=True)
