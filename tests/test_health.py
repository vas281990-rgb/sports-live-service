from fastapi.testclient import TestClient

from app.main import app

# Create a virtual test client to simulate HTTP requests without running a real server
client = TestClient(app)


def test_healthcheck():
    # Send a GET request to the health check endpoint
    response = client.get("/api/v1/health")
    # Assert that the HTTP status code is 200 (Success)
    assert response.status_code == 200
    # Verify that the response body contains the expected status message
    assert response.json() == {"status": "ok"}