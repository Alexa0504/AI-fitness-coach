import json
from datetime import datetime, timedelta
from backend.models import User


def test_xp_add_basic(app, client, user, auth_header):
    user.xp = 0
    user.level = 1

    rv = client.patch("/api/xp/update", headers=auth_header, json={"xp_gain": 300})
    assert rv.status_code == 200
    data = rv.get_json()

    assert data["xp"] == 300
    assert data["level"] == 1


def test_xp_levelup(app, client, user, auth_header):
    user.xp = 1000
    user.level = 1

    rv = client.patch("/api/xp/update", headers=auth_header, json={"xp_gain": 300})
    assert rv.status_code == 200
    data = rv.get_json()

    assert data["level"] == 2
    assert data["xp"] == 100


def test_xp_multiple_levelups(app, client, user, auth_header):
    user.xp = 1100
    user.level = 1

    rv = client.patch("/api/xp/update", headers=auth_header, json={"xp_gain": 2500})
    assert rv.status_code == 200
    data = rv.get_json()

    assert data["level"] == 4
    assert data["xp"] == 0


def test_xp_status_endpoint(app, client, user, auth_header):
    rv = client.get("/api/xp/status", headers=auth_header)
    assert rv.status_code == 200
    data = rv.get_json()

    assert "xp" in data
    assert "level" in data
    assert "xp_to_next_level" in data


def test_xp_negative_gain(app, client, user, auth_header):
    rv = client.patch("/api/xp/update", headers=auth_header, json={"xp_gain": -10})
    assert rv.status_code == 400


def test_xp_missing_field(app, client, user, auth_header):
    rv = client.patch("/api/xp/update", headers=auth_header, json={})
    assert rv.status_code == 400


def test_level_does_not_drop(app, client, user, auth_header):
    user.xp = 50
    user.level = 3
    rv = client.patch("/api/xp/update", headers=auth_header, json={"xp_gain": 0})
    data = rv.get_json()
    assert data["level"] == 3


def test_xp_carry_over_correct(app, client, user, auth_header):
    user.xp = 1199
    user.level = 1
    rv = client.patch("/api/xp/update", headers=auth_header, json={"xp_gain": 10})
    data = rv.get_json()

    assert data["level"] == 2
    assert data["xp"] == 9


def test_xp_large_value_no_error(app, client, user, auth_header):
    rv = client.patch("/api/xp/update", headers=auth_header, json={"xp_gain": 100000})
    assert rv.status_code == 200


def test_xp_update_requires_auth(client):
    rv = client.patch("/api/xp/update", json={"xp_gain": 100})
    assert rv.status_code == 401