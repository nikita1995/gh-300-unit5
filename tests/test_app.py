import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_signup_and_unregister():
    # Use a known activity and a test email
    activity = list(client.get("/activities").json().keys())[0]
    email = "pytestuser@example.com"
    # Sign up
    signup_resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup_resp.status_code == 200 or signup_resp.status_code == 400  # 400 if already signed up
    # Unregister
    unregister_resp = client.post(f"/activities/{activity}/unregister?email={email}")
    assert unregister_resp.status_code == 200 or unregister_resp.status_code == 400  # 400 if not signed up

def test_signup_invalid_activity():
    resp = client.post("/activities/NonexistentActivity/signup?email=pytestuser@example.com")
    assert resp.status_code == 404

def test_unregister_invalid_activity():
    resp = client.post("/activities/NonexistentActivity/unregister?email=pytestuser@example.com")
    assert resp.status_code == 404
