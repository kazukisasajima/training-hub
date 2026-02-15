def test_create_user_success(client):
    r = client.post("/users", json={"email": "a@example.com", "password": "password123"})
    assert r.status_code == 201, r.text
    body = r.json()
    assert body["email"] == "a@example.com"
    assert "id" in body
    assert body["is_active"] is True


def test_create_user_conflict(client):
    client.post("/users", json={"email": "dup@example.com", "password": "password123"})
    r = client.post("/users", json={"email": "dup@example.com", "password": "password123"})
    assert r.status_code == 409, r.text
    body = r.json()
    assert body["code"] == "CONFLICT"


def test_get_user_not_found(client):
    r = client.get("/users/999999")
    assert r.status_code == 404, r.text
    body = r.json()
    assert body["code"] == "NOT_FOUND"


def test_list_users(client):
    # 最低限：空でも200、作ったら増える
    r0 = client.get("/users")
    assert r0.status_code == 200, r0.text

    client.post("/users", json={"email": "list1@example.com", "password": "password123"})
    r1 = client.get("/users")
    assert r1.status_code == 200, r1.text
    assert isinstance(r1.json(), list)
    assert any(u["email"] == "list1@example.com" for u in r1.json())
