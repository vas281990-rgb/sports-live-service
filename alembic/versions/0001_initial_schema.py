"""initial schema

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-05-14
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "raw_snapshots",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("source", sa.String(length=64), nullable=False),
        sa.Column("fixture_name", sa.String(length=255), nullable=True),
        sa.Column("payload", postgresql.JSONB(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_raw_snapshots_source", "raw_snapshots", ["source"])

    op.create_table(
        "teams",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("external_id", sa.Integer(), nullable=False, unique=True),
        sa.Column("name", sa.String(length=255), nullable=False),
    )
    op.create_index("ix_teams_external_id", "teams", ["external_id"])

    op.create_table(
        "tournaments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("external_id", sa.Integer(), nullable=False, unique=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("category_name", sa.String(length=255), nullable=True),
    )
    op.create_index("ix_tournaments_external_id", "tournaments", ["external_id"])

    op.create_table(
        "events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("external_id", sa.Integer(), nullable=False, unique=True),
        sa.Column("tournament_id", sa.Integer(), sa.ForeignKey("tournaments.id"), nullable=False),
        sa.Column("home_team_id", sa.Integer(), sa.ForeignKey("teams.id"), nullable=False),
        sa.Column("away_team_id", sa.Integer(), sa.ForeignKey("teams.id"), nullable=False),
        sa.Column("status", sa.String(length=64), nullable=False),
        sa.Column("status_description", sa.String(length=255), nullable=True),
        sa.Column("is_editor", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("start_time", sa.DateTime(timezone=True), nullable=True),
        sa.Column("upstream_updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_events_external_id", "events", ["external_id"])
    op.create_index("ix_events_is_editor", "events", ["is_editor"])
    op.create_index("ix_events_hot_path", "events", ["is_editor", "status", "updated_at"])

    op.create_table(
        "scores",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("event_id", sa.Integer(), sa.ForeignKey("events.id"), nullable=False, unique=True),
        sa.Column("home_current", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("away_current", sa.Integer(), nullable=False, server_default="0"),
    )
    op.create_index("ix_scores_event_id", "scores", ["event_id"])

    op.create_table(
        "backfill_checkpoints",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("source", sa.String(length=64), nullable=False, unique=True),
        sa.Column("last_cursor", sa.String(length=255), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )


def downgrade():
    op.drop_table("backfill_checkpoints")
    op.drop_index("ix_scores_event_id", table_name="scores")
    op.drop_table("scores")
    op.drop_index("ix_events_hot_path", table_name="events")
    op.drop_index("ix_events_is_editor", table_name="events")
    op.drop_index("ix_events_external_id", table_name="events")
    op.drop_table("events")
    op.drop_index("ix_tournaments_external_id", table_name="tournaments")
    op.drop_table("tournaments")
    op.drop_index("ix_teams_external_id", table_name="teams")
    op.drop_table("teams")
    op.drop_index("ix_raw_snapshots_source", table_name="raw_snapshots")
    op.drop_table("raw_snapshots")