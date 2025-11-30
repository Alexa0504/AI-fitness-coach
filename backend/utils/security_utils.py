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

def hash_password(password: str) -> str:
    password_bytes = password.encode('utf-8')
    return bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode('utf-8')


def check_password(password: str, hashed_password: str) -> bool:
    password_bytes = password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)


# --- Authentication (JWT) Functions ---

def generate_auth_token(user_id: str) -> str | None:
    SECRET_KEY = _get_secret_key()
    if not SECRET_KEY:
        return None

    try:
        payload = {
            'exp': datetime.now(timezone.utc) + timedelta(days=TOKEN_EXPIRY_DAYS),
            'iat': datetime.now(timezone.utc),
            'sub': user_id
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
