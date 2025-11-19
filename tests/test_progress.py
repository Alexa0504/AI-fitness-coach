import json
from datetime import datetime, timedelta
from backend.models import User

def test_progress_save_basic(app, client, user, auth_header):
    rv = client.patch("/api/progress/save", headers=auth_header, json={"progress": {"workout": 50}})
    assert rv.status_code == 200
    data = rv.get_json()
    assert data["progress_saved_state"]["workout"] == 50


def test_progress_save_overwrites(app, client, user, auth_header):
    user.set_progress_state({"workout": 10})
    rv = client.patch("/api/progress/save", headers=auth_header, json={"progress": {"workout": 80}})
    data = rv.get_json()
    assert data["progress_saved_state"]["workout"] == 80


def test_progress_save_invalid_body(app, client, user, auth_header):
    rv = client.patch("/api/progress/save", headers=auth_header, json={})
    assert rv.status_code == 400


def test_progress_save_non_json(app, client, user, auth_header):
    rv = client.patch("/api/progress/save", headers=auth_header, data="notjson")
    assert rv.status_code == 400


def test_progress_save_updates_timestamp(app, client, user, auth_header):
    user.last_progress_update = datetime.utcnow() - timedelta(days=1)
    rv = client.patch("/api/progress/save", headers=auth_header, json={"progress": {"diet": 60}})
    assert rv.status_code == 200

    user_from_db = User.query.get(user.id)
    assert (datetime.utcnow() - user_from_db.last_progress_update).seconds < 3


def test_progress_save_persists_in_db(app, client, user, auth_header):
    client.patch("/api/progress/save", headers=auth_header, json={"progress": {"diet": 33}})
    u = User.query.get(user.id)
    assert u.get_progress_state()["diet"] == 33


def test_progress_save_requires_auth(client):
    rv = client.patch("/api/progress/save", json={"progress": {"x": 1}})
    assert rv.status_code == 401


def test_progress_save_partial_update(app, client, user, auth_header):
    user.set_progress_state({"workout": 10})
    rv = client.patch("/api/progress/save", headers=auth_header, json={"progress": {"diet": 20}})
    data = rv.get_json()

    assert data["progress_saved_state"]["workout"] == 10
    assert data["progress_saved_state"]["diet"] == 20


def test_progress_save_handles_string_state(app, client, user, auth_header):
    user.progress_saved_state = '{"workout": 5}'
    rv = client.patch("/api/progress/save", headers=auth_header, json={"progress": {"workout": 15}})
    data = rv.get_json()
    assert data["progress_saved_state"]["workout"] == 15


def test_progress_save_empty_object(app, client, user, auth_header):
    rv = client.patch("/api/progress/save", headers=auth_header, json={"progress": {}})
    assert rv.status_code == 200