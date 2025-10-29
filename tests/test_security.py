from datetime import datetime, timedelta, timezone
import jwt
import os
from unittest.mock import patch, MagicMock

import pytest

from backend.utils import security_utils

TEST_SECRET_KEY = "test-ai-fitness-coach-secret-key-123"


# --- Setup Fixture ---

@pytest.fixture(autouse=True)
def set_test_env():
    """Sets the SECRET_KEY for the duration of the tests."""
    with patch.dict(os.environ, {"SECRET_KEY": TEST_SECRET_KEY}):
        yield  # This allows the tests to run


# --- Password Hashing Tests ---

def test_hash_and_check_password_success():
    """Tests that hashing and checking the password work successfully."""
    password = "MySecurePassword123"
    hashed = security_utils.hash_password(password)

    # 1. Check that the hash is of type bytes and is long (not empty)
    assert isinstance(hashed, bytes)
    assert len(hashed) > 10

    # 2. Check that check_password returns True for the correct password
    assert security_utils.check_password(password, hashed) is True


def test_hash_and_check_password_failure():
    """Tests that check_password returns False for an incorrect password."""
    password = "MySecurePassword123"
    wrong_password = "WrongPassword456"
    hashed = security_utils.hash_password(password)

    # Check that check_password returns False for the incorrect password
    assert security_utils.check_password(wrong_password, hashed) is False


def test_hash_is_unique():
    """Tests that hashing two identical passwords results in different hashes (due to the salt)."""
    password = "MySecurePassword123"
    hashed1 = security_utils.hash_password(password)
    hashed2 = security_utils.hash_password(password)

    assert hashed1 != hashed2


# --- Token Logic Tests ---

def test_token_generation_and_decoding_success():
    """Tests token generation and successful decoding."""
    user_id = "test-user-123"
    token = security_utils.generate_auth_token(user_id)

    assert isinstance(token, str)
    assert token != ""

    # Check decoding
    decoded_user_id = security_utils.decode_auth_token(token)

    assert decoded_user_id == user_id


def test_token_expiration_failure(mocker):
    """
    Tests that decoding an expired token fails (ExpiredSignatureError).
    We use Mocker (pytest-mock) to manipulate the time.
    """
    user_id = "expired-user"
    # Create a token that expired in the past
    past_time = datetime.now(timezone.utc) - timedelta(minutes=5)
    expired_payload = {
        'exp': past_time,
        'iat': past_time - timedelta(minutes=1),
        'sub': user_id
    }

    expired_token = jwt.encode(
        expired_payload,
        TEST_SECRET_KEY,
        algorithm="HS256"
    )

    decoded = security_utils.decode_auth_token(expired_token)

    assert decoded is None


def test_token_invalid_signature_failure():
    """Tests that tokens encoded with a wrong secret key are rejected by the system."""
    user_id = "invalid-sig-user"

    wrong_key = "THIS-IS-A-WRONG-SECRET-KEY"

    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(days=1),
        'iat': datetime.now(timezone.utc),
        'sub': user_id
    }
    invalid_token = jwt.encode(
        payload,
        wrong_key,
        algorithm="HS256"
    )

    decoded = security_utils.decode_auth_token(invalid_token)

    assert decoded is None