from backend.models import db, TokenBlacklist
from datetime import datetime

def add_token_to_blacklist(token: str):
    """Add a JWT token to the blacklist (e.g. during logout)."""
    if not token:
        return False

    blacklisted = TokenBlacklist(token=token, blacklisted_on=datetime.utcnow())
    db.session.add(blacklisted)
    db.session.commit()
    return True

def is_token_blacklisted(token: str) -> bool:
    """Check if a JWT token is already blacklisted."""
    if not token:
        return False

    return db.session.query(
        db.exists().where(TokenBlacklist.token == token)
    ).scalar()
