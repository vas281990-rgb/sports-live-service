from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, aliased

from app.core.database import get_db
from app.models.event import Event
from app.models.score import Score
from app.models.team import Team
from app.models.tournament import Tournament
from app.schemas.live_event import LiveEventsResponse

router = APIRouter()


@router.get(
    "/sport/football/events/live",
    response_model=LiveEventsResponse,
)
def get_live_football_events(
    db: Session = Depends(get_db),
):
    # Hot path reads only normalized tables, never raw JSON.
    HomeTeam = aliased(Team)
    AwayTeam = aliased(Team)

    rows = (
        db.query(Event, Tournament, HomeTeam, AwayTeam, Score)
        .join(Tournament, Tournament.id == Event.tournament_id)
        .join(HomeTeam, HomeTeam.id == Event.home_team_id)
        .join(AwayTeam, AwayTeam.id == Event.away_team_id)
        .join(Score, Score.event_id == Event.id)
        .filter(Event.is_editor.is_(False))
        .order_by(Event.updated_at.desc())
        .all()
    )

    events = []
    for event, tournament, home_team, away_team, score in rows:
        events.append(
            {
                "id": event.external_id,
                "tournament": {
                    "id": tournament.external_id,
                    "name": tournament.name,
                    "category": {"name": tournament.category_name},
                },
                "homeTeam": {"id": home_team.external_id, "name": home_team.name},
                "awayTeam": {"id": away_team.external_id, "name": away_team.name},
                "homeScore": {"current": score.home_current},
                "awayScore": {"current": score.away_current},
                "status": {
                    "type": event.status,
                    "description": event.status_description,
                },
                "isEditor": event.is_editor,
                "startTimestamp": event.start_time,
                "lastUpdatedAt": event.upstream_updated_at,
            }
        )

    return {"events": events}