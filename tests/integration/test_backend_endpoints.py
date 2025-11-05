# ---------------------------
# AUTH INTEGRATION TESTS
# ---------------------------
def test_register_and_login(client):
    # REGISTER
    response = client.post("/api/auth/register", json={
        "username": "alice",
        "email": "alice@test.com",
        "password": "pass123"
    })
    assert response.status_code == 201
    assert "token" in response.get_json()

    # LOGIN
    response = client.post("/api/auth/login", json={
        "email": "alice@test.com",
        "password": "pass123"
    })
    assert response.status_code == 200
    assert "token" in response.get_json()


def test_logout_blacklist(client, auth_header):
    response = client.post("/api/auth/logout", headers=auth_header)
    assert response.status_code == 200
    token = auth_header["Authorization"].split(" ")[1]

    from backend.utils.token_blacklist import is_token_blacklisted
    assert is_token_blacklisted(token)


# ---------------------------
# GOALS INTEGRATION TESTS
# ---------------------------
def test_create_get_update_delete_goal(client, auth_header):
    # CREATE
    response = client.post("/api/goals/", headers=auth_header, json={
        "goal_type": "weight_loss",
        "target_value": 5,
        "unit": "kg"
    })
    goal_id = response.get_json()["goal"]["id"]
    assert response.status_code == 201

    # GET
    response = client.get("/api/goals/", headers=auth_header)
    assert response.status_code == 200
    assert any(g["id"] == goal_id for g in response.get_json())

    # UPDATE
    response = client.put(f"/api/goals/{goal_id}", headers=auth_header, json={"target_value": 6})
    assert response.status_code == 200
    assert response.get_json()["goal"]["target_value"] == 6

    # DELETE
    response = client.delete(f"/api/goals/{goal_id}", headers=auth_header)
    assert response.status_code == 200


# ---------------------------
# PLANS INTEGRATION TESTS
# ---------------------------
def test_create_get_update_delete_plan(client, auth_header):
    # CREATE
    response = client.post("/api/plans/", headers=auth_header, json={"plan_type": "workout"})
    plan_id = response.get_json()["plan"]["id"]
    assert response.status_code == 201

    # GET ALL
    response = client.get("/api/plans/", headers=auth_header)
    assert response.status_code == 200
    assert any(p["id"] == plan_id for p in response.get_json())

    # GET SINGLE
    response = client.get(f"/api/plans/{plan_id}", headers=auth_header)
    assert response.status_code == 200

    # UPDATE
    response = client.put(f"/api/plans/{plan_id}", headers=auth_header, json={"plan_type": "diet"})
    assert response.status_code == 200
    assert response.get_json()["plan"]["plan_type"] == "diet"

    # DELETE
    response = client.delete(f"/api/plans/{plan_id}", headers=auth_header)
    assert response.status_code == 200


# ---------------------------
# TOKEN REQUIRED DECORATOR TEST
# ---------------------------
def test_protected_route_requires_token(client):
    response = client.get("/api/goals/")
    assert response.status_code == 401
    assert "Token is missing" in response.get_json()["message"]
