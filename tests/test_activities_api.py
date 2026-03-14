import pytest


def test_get_activities(client):
    response = client.get("/activities")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_activity(client):
    payload_email = "newstudent@mergington.edu"
    response = client.post("/activities/Chess%20Club/signup?email=" + payload_email)
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]

    updated = client.get("/activities").json()
    assert payload_email in updated["Chess Club"]["participants"]


def test_signup_duplicate_returns_400(client):
    payload_email = "duplicate@mergington.edu"
    client.post("/activities/Chess%20Club/signup?email=" + payload_email)
    response = client.post("/activities/Chess%20Club/signup?email=" + payload_email)

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_delete_participant(client):
    payload_email = "delete_me@mergington.edu"
    client.post("/activities/Chess%20Club/signup?email=" + payload_email)

    response = client.delete("/activities/Chess%20Club/participants?email=" + payload_email)
    assert response.status_code == 200
    assert f"Removed {payload_email}" in response.json()["message"]

    updated = client.get("/activities").json()
    assert payload_email not in updated["Chess Club"]["participants"]


def test_delete_nonexistent_participant_404(client):
    response = client.delete("/activities/Chess%20Club/participants?email=notexist@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not registered for this activity"


def test_activity_not_found_404(client):
    response = client.post("/activities/NoSuchActivity/signup?email=student@mergington.edu")
    assert response.status_code == 404

    response = client.delete("/activities/NoSuchActivity/participants?email=student@mergington.edu")
    assert response.status_code == 404
