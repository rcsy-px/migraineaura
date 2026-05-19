"""initial migraine journal schema

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-05-19
"""
from alembic import op
import sqlalchemy as sa

revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=80), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )
    op.create_index(op.f("ix_users_username"), "users", ["username"], unique=False)
    op.create_table(
        "migraine_events",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("event_date", sa.Date(), nullable=False),
        sa.Column("event_time", sa.Time(), nullable=False),
        sa.Column("duration_minutes", sa.Integer(), nullable=True),
        sa.Column("event_type", sa.String(length=40), nullable=False),
        sa.Column("aura_intensity", sa.Integer(), nullable=False),
        sa.Column("headache_intensity", sa.Integer(), nullable=False),
        sa.Column("headache_started_after_minutes", sa.Integer(), nullable=True),
        sa.Column("numbness", sa.Boolean(), nullable=False),
        sa.Column("speech_problems", sa.Boolean(), nullable=False),
        sa.Column("weakness", sa.Boolean(), nullable=False),
        sa.Column("confusion", sa.Boolean(), nullable=False),
        sa.Column("unusual_event", sa.Boolean(), nullable=False),
        sa.Column("identical_to_usual_pattern", sa.Boolean(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("possible_trigger_notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_migraine_events_event_date"), "migraine_events", ["event_date"], unique=False)
    op.create_index(op.f("ix_migraine_events_user_id"), "migraine_events", ["user_id"], unique=False)
    op.create_table(
        "event_visual_symptoms",
        sa.Column("event_id", sa.Integer(), nullable=False),
        sa.Column("symptom", sa.String(length=40), nullable=False),
        sa.ForeignKeyConstraint(["event_id"], ["migraine_events.id"]),
        sa.PrimaryKeyConstraint("event_id", "symptom"),
    )
    op.create_table(
        "recovery_data",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("event_id", sa.Integer(), nullable=False),
        sa.Column("fatigue_after", sa.Boolean(), nullable=False),
        sa.Column("brain_fog", sa.Boolean(), nullable=False),
        sa.Column("irritability", sa.Boolean(), nullable=False),
        sa.Column("recovery_hours", sa.Integer(), nullable=True),
        sa.Column("sleep_after_event", sa.Boolean(), nullable=False),
        sa.Column("returned_to_normal", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["event_id"], ["migraine_events.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("event_id"),
    )
    op.create_table(
        "trigger_contexts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("event_id", sa.Integer(), nullable=False),
        sa.Column("sleep_hours", sa.Numeric(precision=3, scale=1), nullable=True),
        sa.Column("sleep_quality", sa.Integer(), nullable=True),
        sa.Column("interrupted_sleep", sa.Boolean(), nullable=False),
        sa.Column("daytime_nap", sa.Boolean(), nullable=False),
        sa.Column("hydration_level", sa.String(length=20), nullable=False),
        sa.Column("caffeine_count", sa.Integer(), nullable=False),
        sa.Column("caffeine_type", sa.String(length=80), nullable=True),
        sa.Column("stress_level", sa.Integer(), nullable=True),
        sa.Column("illness_type", sa.String(length=40), nullable=False),
        sa.Column("screen_time_level", sa.String(length=20), nullable=False),
        sa.ForeignKeyConstraint(["event_id"], ["migraine_events.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("event_id"),
    )
    op.create_table(
        "trigger_meal_flags",
        sa.Column("context_id", sa.Integer(), nullable=False),
        sa.Column("flag", sa.String(length=40), nullable=False),
        sa.ForeignKeyConstraint(["context_id"], ["trigger_contexts.id"]),
        sa.PrimaryKeyConstraint("context_id", "flag"),
    )


def downgrade():
    op.drop_table("trigger_meal_flags")
    op.drop_table("trigger_contexts")
    op.drop_table("recovery_data")
    op.drop_table("event_visual_symptoms")
    op.drop_index(op.f("ix_migraine_events_user_id"), table_name="migraine_events")
    op.drop_index(op.f("ix_migraine_events_event_date"), table_name="migraine_events")
    op.drop_table("migraine_events")
    op.drop_index(op.f("ix_users_username"), table_name="users")
    op.drop_table("users")
