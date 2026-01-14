import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from .config import settings

def hash_password(raw: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(raw.encode("utf-8"), salt)
    return hashed.decode("utf-8")

def verify_password(raw: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(raw.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False

def create_jwt(uid: int, sid: str) -> str:
    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=settings.jwt_expire_minutes)
    payload = {
        "uid": uid,
        "sid": sid,
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
    }
    return jwt.encode(payload, settings.secret_key, algorithm="HS256")

def decode_jwt(token: str) -> dict:
    return jwt.decode(token, settings.secret_key, algorithms=["HS256"])

def session_expires_at() -> datetime:
    return datetime.now(timezone.utc) + timedelta(days=settings.session_expire_days)
