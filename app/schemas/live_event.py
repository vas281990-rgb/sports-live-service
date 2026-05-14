from datetime import datetime

from pydantic import BaseModel


class TeamSchema(BaseModel):
    id: int
    name: str


class TournamentCategorySchema(BaseModel):
    name: str | None = None


class TournamentSchema(BaseModel):
    id: int
    name: str
    category: TournamentCategorySchema


class StatusSchema(BaseModel):
    type: str
    description: str | None = None


class ScoreSchema(BaseModel):
    current: int


class LiveEventSchema(BaseModel):
    id: int
    tournament: TournamentSchema
    homeTeam: TeamSchema
    awayTeam: TeamSchema
    homeScore: ScoreSchema
    awayScore: ScoreSchema
    status: StatusSchema
    isEditor: bool
    startTimestamp: datetime | None = None
    lastUpdatedAt: datetime | None = None


class LiveEventsResponse(BaseModel):
    events: list[LiveEventSchema]