def test_fixture_contains_editor_and_non_editor_events():
    # Define a test data structure (fixture) containing both editor and non-editor events
    fixture = {
        "events": [
            {"id": 1, "isEditor": True},
            {"id": 2, "isEditor": False},
        ]
    }
    # Filter the list to extract only events where "isEditor" is True
    editor_events = [
        event for event in fixture["events"]
        if event["isEditor"] is True
    ]
    # Assert that exactly one editor event was found
    assert len(editor_events) == 1
    # Verify that the filtered event has the correct ID
    assert editor_events[0]["id"] == 1