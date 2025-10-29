import bcrypt
import jwt
import os  # ÚJ: Importáljuk az 'os' modult a környezeti változókhoz
from datetime import datetime, timedelta, timezone

# --- Configuration Loading ---

# We load the secret key from an environment variable.
SECRET_KEY = os.getenv("SECRET_KEY",
                       "DEFAULT_FALLBACK_KEY_IF_ENV_MISSING")  # Emergency fallback
ALGORITHM = "HS256"
TOKEN_EXPIRY_DAYS = 1


# --- Password Management Functions ---

def hash_password(password: str) -> bytes:
    """
    Safely hashes the given password using the bcrypt algorithm.
    Returns the hashed password as bytes (this should be stored in the database).
    """
    # Encoding the password as bytes is required for bcrypt
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
    if not SECRET_KEY or SECRET_KEY == "DEFAULT_FALLBACK_KEY_IF_ENV_MISSING":
        print("FATAL: SECRET_KEY is missing or using fallback. Token generation failed.")
        return None

    try:
        # The JWT payload data
        payload = {
            'exp': datetime.now(timezone.utc) + timedelta(days=TOKEN_EXPIRY_DAYS),  # Expiration time
            'iat': datetime.now(timezone.utc),  # Issued At time
            'sub': user_id  # Subject - the user identifier
        }
        # Encoding with the secret key
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
    if not SECRET_KEY or SECRET_KEY == "DEFAULT_FALLBACK_KEY_IF_ENV_MISSING":
        print("FATAL: SECRET_KEY is missing or using fallback. Token decoding failed.")
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