import pytest
from backend.utils import token_blacklist
from backend.models import db, TokenBlacklist

@pytest.fixture
def setup_db(app):
    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()

def test_add_token_to_blacklist_true(setup_db):
    result = token_blacklist.add_token_to_blacklist("mocktoken")
    assert result is True
    token = db.session.query(TokenBlacklist).filter_by(token="mocktoken").first()
    assert token is not None

def test_add_token_to_blacklist_false(setup_db):
    result = token_blacklist.add_token_to_blacklist(None)
    assert result is False

def test_is_token_blacklisted(setup_db):
    token_blacklist.add_token_to_blacklist("checktoken")
    assert token_blacklist.is_token_blacklisted("checktoken") is True
    assert token_blacklist.is_token_blacklisted("notoken") is False
