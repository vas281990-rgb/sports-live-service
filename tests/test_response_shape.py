def test_sofascore_like_response_shape():
    # Create a mock response that mimics the real SofaScore API structure
    response = {
        "events": [
            {
                "id": 1001,
                "tournament": {
                    "id": 77,
                    "name": "La Liga",
                    "category": {"name": "Spain"},
                },
                "homeTeam": {"id": 1, "name": "Barcelona"},
                "awayTeam": {"id": 2, "name": "Real Madrid"},
                "homeScore": {"current": 2},
                "awayScore": {"current": 1},
                "status": {"type": "inprogress", "description": "Live"},
                "isEditor": True,
                "startTimestamp": "2026-05-14T18:00:00Z",
                "lastUpdatedAt": "2026-05-14T18:00:05Z",
            }
        ]
    }
    # Access the first event in the mocked response list
    event = response["events"][0]
    # Ensure all mandatory keys exist in the event object
    assert "homeTeam" in event
    assert "awayTeam" in event
    assert "tournament" in event
    assert "homeScore" in event
    assert "awayScore" in event
    # Verify the boolean value for the isEditor field
    assert event["isEditor"] is True