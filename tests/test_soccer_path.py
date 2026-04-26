import sys
import os
from fastapi.testclient import TestClient

# SYSTEM CONFIGURATION: Ensuring Python finds the backend directory 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.main import app

# INITIALIZING THE TEST CLIENT
client = TestClient(app)

# 1. TEST: Root API Connection (Read)
def test_read_root():
    """Verifies if the API is active and returning the correct welcome message."""
    response = client.get("/")
    assert response.status_code == 200
    assert "SoccerPath AI System Active" in response.json()["message"]

# 2. TEST: Athlete Performance History (Read)
def test_get_performance():
    """Checks if the athlete profile and match history are being retrieved correctly."""
    response = client.get("/my-performance")
    assert response.status_code == 200
    assert response.json()["athlete"] == "Pedro Henrique"
    assert "Tabor College" in response.json()["college"]

# 3. TEST: Adding Match Stats (Create)
def test_add_match():
    """Simulates adding a new match and verifies the AI Coach feedback."""
    response = client.post("/add-match?goals=1&assists=1&interceptions=2")
    assert response.status_code == 200
    assert "status" in response.json()
    assert "coach_feedback" in response.json()

# 4. TEST: Error Handling for Non-Existent Record (Delete)
def test_delete_invalid_match():
    """Ensures the system returns a 404 error when trying to delete a non-existent ID."""
    response = client.delete("/delete-match/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Match not found."

# 5. TEST: Error Handling for Non-Existent Record 
def test_update_invalid_match():
    """Ensures the system returns a 404 error when trying to update a non-existent ID."""
    response = client.put("/update-match/99999?goals=5&assists=5&interceptions=5")
    assert response.status_code == 404
    assert response.json()["detail"] == "Match not found."