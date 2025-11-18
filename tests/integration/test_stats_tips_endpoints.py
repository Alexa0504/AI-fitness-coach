import pytest
import json
from backend.models import Tip, db


@pytest.mark.usefixtures("seed_tips")
def test_tips_returned(client):
    response = client.get("/tips/general/weekly")
    data = json.loads(response.data)
    assert response.status_code == 200
    assert len(data) > 0


@pytest.mark.usefixtures("seed_tips")
def test_tips_max_three(client):
    response = client.get("/tips/general/weekly")
    data = json.loads(response.data)
    assert len(data) <= 3


@pytest.mark.usefixtures("seed_tips")
def test_tips_random_selection(client):
    response1 = client.get("/tips/general/weekly")
    response2 = client.get("/tips/general/weekly")
    data1 = json.loads(response1.data)
    data2 = json.loads(response2.data)
    assert data1 != data2 or len(data1) < 2


@pytest.mark.usefixtures("seed_tips")
def test_tips_empty_category(client):
    response = client.get("/tips/nonexistent/weekly")
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data == []


@pytest.mark.usefixtures("seed_tips")
def test_tips_structure(client):
    response = client.get("/tips/general/weekly")
    data = json.loads(response.data)
    for tip in data:
        assert "id" in tip
        assert "category" in tip
        assert "text" in tip


@pytest.mark.usefixtures("seed_tips")
def test_tips_specific_text(client, app):
    with app.app_context():
        tip = Tip.query.filter_by(text="Eat more vegetables").first()
        assert tip is not None


@pytest.mark.usefixtures("seed_tips")
def test_less_than_three_tips(client, app):
    with app.app_context():
        db.session.query(Tip).delete()
        db.session.add(Tip(category="general", text="Only one tip"))
        db.session.commit()

    response = client.get("/tips/general/weekly")
    data = json.loads(response.data)
    assert len(data) == 1


@pytest.mark.usefixtures("seed_tips")
def test_multiple_categories(client):
    response = client.get("/tips/general/weekly")
    data = json.loads(response.data)
    for tip in data:
        assert tip["category"] in ["general", "workout", "sleep", "nutrition"]


@pytest.mark.usefixtures("seed_tips")
def test_tips_json_format(client):
    response = client.get("/tips/general/weekly")
    assert response.headers["Content-Type"] == "application/json"


@pytest.mark.usefixtures("seed_tips")
def test_tips_randomness_over_multiple_calls(client):
    responses = [json.loads(client.get("/tips/general/weekly").data) for _ in range(5)]
    all_same = all(r == responses[0] for r in responses)
    if len(responses[0]) > 1:
        assert not all_same
