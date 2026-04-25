import sys
import os
from fastapi.testclient import TestClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from main import app
from models import Winger, Fullback

client = TestClient(app)

def test_winger_metrics_count():
    player = Winger("Pedro", "Tabor College")
    metrics = player.get_role_metrics()
    assert len(metrics) == 3 

def test_read_main_route():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "SoccerPath AI Active"}

def test_invalid_position_analysis():
    response = client.post("/analyze/Referee", json={"stats": {}})
