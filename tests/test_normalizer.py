from app.services.normalizer import parse_datetime


def test_parse_datetime_zulu():
    """parse_datetime correctly converts Zulu ISO timestamp to aware datetime."""
    result = parse_datetime("2026-05-14T18:00:00Z")
    assert result is not None
    assert result.tzinfo is not None
    assert result.year == 2026
    assert result.hour == 18


def test_parse_datetime_none_returns_none():
    """parse_datetime returns None when given None."""
    assert parse_datetime(None) is None


def test_parse_datetime_empty_string_returns_none():
    """parse_datetime returns None when given empty string."""
    assert parse_datetime("") is None


def test_parse_datetime_preserves_minutes():
    """parse_datetime correctly parses minutes."""
    result = parse_datetime("2026-05-14T18:30:05Z")
    assert result is not None
    assert result.minute == 30
    assert result.second == 5