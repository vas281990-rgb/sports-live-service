from datetime import datetime, timezone
from typing import Any

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.models.event import Event
from app.models.raw_snapshot import RawSnapshot
from app.models.score import Score
from app.models.team import Team
from app.models.tournament import Tournament


def parse_datetime(value: str | None):
    if not value:
        return None
    # Convert Zulu time to Python-compatible UTC offset.
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def upsert_team(db: Session, team_payload: dict[str, Any]) -> int:
    stmt = (
        insert(Team)
        .values(
            external_id=team_payload["id"],
            name=team_payload["name"],
        )
        .on_conflict_do_update(
            index_elements=[Team.external_id],
            set_={
                "name": team_payload["name"],
            },
        )
        .returning(Team.id)
    )
    return db.execute(stmt).scalar_one()


def upsert_tournament(db: Session, payload: dict[str, Any]) -> int:
    category = payload.get("category") or {}
    stmt = (
        insert(Tournament)
        .values(
            external_id=payload["id"],
            name=payload["name"],
            category_name=category.get("name"),
        )
        .on_conflict_do_update(
            index_elements=[Tournament.external_id],
            set_={
                "name": payload["name"],
                "category_name": category.get("name"),
            },
        )
        .returning(Tournament.id)
    )
    return db.execute(stmt).scalar_one()


def upsert_event(
    db: Session,
    item: dict[str, Any],
    tournament_id: int,
    home_team_id: int,
    away_team_id: int,
) -> int:
    status = item.get("status") or {}
    now = datetime.now(timezone.utc)  # explicit UTC for upsert updated_at

    stmt = (
        insert(Event)
        .values(
            external_id=item["id"],
            tournament_id=tournament_id,
            home_team_id=home_team_id,
            away_team_id=away_team_id,
            status=status.get("type", "unknown"),
            status_description=status.get("description"),
            is_editor=item.get("isEditor", False),
            start_time=parse_datetime(item.get("startTimestamp")),
            upstream_updated_at=parse_datetime(item.get("lastUpdatedAt")),
        )
        .on_conflict_do_update(
            index_elements=[Event.external_id],
            set_={
                "tournament_id": tournament_id,
                "home_team_id": home_team_id,
                "away_team_id": away_team_id,
                "status": status.get("type", "unknown"),
                "status_description": status.get("description"),
                "is_editor": item.get("isEditor", False),
                "start_time": parse_datetime(item.get("startTimestamp")),
                "upstream_updated_at": parse_datetime(item.get("lastUpdatedAt")),
                # FIX: onupdate=func.now() does NOT fire on raw INSERT..ON CONFLICT.
                # Must set updated_at explicitly here.
                "updated_at": now,
            },
        )
        .returning(Event.id)
    )
    return db.execute(stmt).scalar_one()


def upsert_score(
    db: Session,
    event_id: int,
    item: dict[str, Any],
) -> None:
    home_score = item.get("homeScore") or {}
    away_score = item.get("awayScore") or {}
    stmt = (
        insert(Score)
        .values(
            event_id=event_id,
            home_current=home_score.get("current", 0),
            away_current=away_score.get("current", 0),
        )
        .on_conflict_do_update(
            index_elements=[Score.event_id],
            set_={
                "home_current": home_score.get("current", 0),
                "away_current": away_score.get("current", 0),
            },
        )
    )
    db.execute(stmt)


def normalize_raw_snapshot(
    db: Session,
    snapshot_id: int,
) -> int:
    snapshot = db.query(RawSnapshot).filter(RawSnapshot.id == snapshot_id).one()
    events = snapshot.payload.get("events", [])
    normalized_count = 0

    # One transaction for the whole snapshot keeps normalization consistent.
    for item in events:
        home_team_id = upsert_team(db, item["homeTeam"])
        away_team_id = upsert_team(db, item["awayTeam"])
        tournament_id = upsert_tournament(db, item["tournament"])
        event_id = upsert_event(
            db=db,
            item=item,
            tournament_id=tournament_id,
            home_team_id=home_team_id,
            away_team_id=away_team_id,
        )
        upsert_score(db, event_id, item)
        normalized_count += 1

    db.commit()
    return normalized_count