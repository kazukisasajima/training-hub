import pytest


@pytest.fixture()
def registered_user(client):
    """Create a user and return their credentials."""
    client.post(
        "/users",
        json={"name": "Auth User", "email": "authuser@example.com", "password": "P@ssw0rd&1"},
    )
    return {"email": "authuser@example.com", "password": "P@ssw0rd&1"}


def test_login_success(client, registered_user):
    r = client.post(
        "/api/auth/login",
        data={"username": registered_user["email"], "password": registered_user["password"]},
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"


def test_login_wrong_password(client, registered_user):
    r = client.post(
        "/api/auth/login",
        data={"username": registered_user["email"], "password": "WrongPass1"},
    )
    assert r.status_code == 401, r.text
    body = r.json()
    assert body["code"] == "UNAUTHORIZED"


def test_login_unknown_email(client):
    r = client.post(
        "/api/auth/login",
        data={"username": "nobody@example.com", "password": "P@ssw0rd&1"},
    )
    assert r.status_code == 401, r.text
    body = r.json()
    assert body["code"] == "UNAUTHORIZED"
