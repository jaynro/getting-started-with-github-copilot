from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    # Basic GET returns a dict containing known activities
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data


def test_signup_and_unregister():
    activity = "Science Club"
    email = "pytest.user@mergington.edu"

    # Ensure user not already in participants
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Signup
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert resp.json()["message"].startswith("Signed up")
    assert email in activities[activity]["participants"]

    # Double-signup should fail
    resp2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp2.status_code == 400

    # Unregister
    resp3 = client.post(f"/activities/{activity}/unregister?email={email}")
    assert resp3.status_code == 200
    assert resp3.json()["message"].startswith("Unregistered")
    assert email not in activities[activity]["participants"]
