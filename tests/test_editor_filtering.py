def test_editor_events_are_excluded():
    # Define fixture with both editor and non-editor events
    fixture = {
        "events": [
            {"id": 1, "isEditor": True},
            {"id": 2, "isEditor": False},
        ]
    }

    # Keep only events that are NOT editor-blocked
    allowed_events = [
        event for event in fixture["events"]
        if event["isEditor"] is False
    ]

    # Only one event should remain after filtering
    assert len(allowed_events) == 1

    # Verify that non-editor event is returned
    assert allowed_events[0]["id"] == 2