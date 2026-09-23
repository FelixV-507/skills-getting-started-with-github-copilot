import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from app import activities, app
from fastapi.testclient import TestClient

client = TestClient(app)


def reset_activities():
    activities["Chess Club"]["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]
    activities["Programming Class"]["participants"] = ["emma@mergington.edu", "sophia@mergington.edu"]


def test_duplicate_signup_is_rejected():
    reset_activities()

    response = client.post("/activities/Chess Club/signup?email=daniel@mergington.edu")

    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()


def test_unregister_removes_participant():
    reset_activities()

    response = client.delete("/activities/Chess Club/participants?email=daniel@mergington.edu")

    assert response.status_code == 200
    assert "daniel@mergington.edu" not in activities["Chess Club"]["participants"]
    assert "michael@mergington.edu" in activities["Chess Club"]["participants"]
