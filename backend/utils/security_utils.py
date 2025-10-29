import bcrypt
import jwt
import os
from datetime import datetime, timedelta, timezone

# --- Globals (Constants) ---

ALGORITHM = "HS256"
TOKEN_EXPIRY_DAYS = 1


# --- Key Retrieval Function (Lazy Loading Fix for Testing) ---

def _get_secret_key() -> str | None:
    """
    Retrieves the SECRET_KEY from the environment variables (os.environ).
    This function implements the 'lazy loading' fix for testing compatibility,
    ensuring the key is read only when an auth function is called.
    """

    key = os.getenv("SECRET_KEY")

    if not key:
        key = "DEFAULT_FALLBACK_KEY_IF_ENV_MISSING"

    if key == "DEFAULT_FALLBACK_KEY_IF_ENV_MISSING":
        print("FATAL: SECRET_KEY is missing or using fallback. Token operation failed.")
        return None

    return key


# --- Password Management Functions ---

def hash_password(password: str) -> bytes:
    """
    Safely hashes the given password using the bcrypt algorithm.
    Returns the hashed password as bytes (this should be stored in the database).
    """
    password_bytes = password.encode('utf-8')
    # Generating salt and hashing simultaneously
    return bcrypt.hashpw(password_bytes, bcrypt.gensalt())


def check_password(password: str, hashed_password: bytes) -> bool:
    """
    Checks if the provided plain password matches the stored hash.
    """
    password_bytes = password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_password)


# --- Authentication (JWT) Functions ---

def generate_auth_token(user_id: str) -> str | None:
    """
    Creates a JWT token with the user identifier.
    The token is valid for TOKEN_EXPIRY_DAYS (1 day).
    Returns the token string or None on failure.
    """
    # Lazy Load: Get the key only when the function runs.
    SECRET_KEY = _get_secret_key()
    if not SECRET_KEY:
        return None

    try:
        payload = {
            'exp': datetime.now(timezone.utc) + timedelta(days=TOKEN_EXPIRY_DAYS),  # Expiration time
            'iat': datetime.now(timezone.utc),  # Issued At time
            'sub': user_id  # Subject - the user identifier
        }
        token = jwt.encode(
            payload,
            SECRET_KEY,
            algorithm=ALGORITHM
        )
        return token
    except Exception as e:
        print(f"Error during token generation: {e}")
        return None


def decode_auth_token(auth_token: str) -> str | None:
    """
    Decodes the JWT token, including validity checks.
    Returns the user identifier (user_id) upon successful decoding, or None on failure.
    """
    # Lazy Load: Get the key only when the function runs.
    SECRET_KEY = _get_secret_key()
    if not SECRET_KEY:
        return None

    try:
        payload = jwt.decode(
            auth_token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload.get('sub')
    except jwt.ExpiredSignatureError:
        print("Error: The authentication token has expired.")
        return None
    except jwt.InvalidTokenError:
        print("Error: Invalid authentication token.")
        return None
    except Exception as e:
        print(f"Unknown error during token decoding: {e}")
        return None