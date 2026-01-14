from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timezone

from app.core.security import hash_password, verify_password, session_expires_at
from .models import User, Session as DbSession

def create_user(db: Session, full_name: str, email: str, password: str) -> User:
    email = email.lower()
    exists = db.query(User).filter(User.email == email).first()
    if exists:
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")

    user = User(full_name=full_name, email=email, password_hash=hash_password(password), is_active=True)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, email: str, password: str) -> User:
    email = email.lower()
    user = db.query(User).filter(User.email == email).first()
    if not user or not user.is_active or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверные данные")
    return user

def create_session(db: Session, user: User, ip: str | None, user_agent: str | None) -> DbSession:
    sess = DbSession(
        user_id=user.id,
        expires_at=session_expires_at(),
        ip=ip,
        user_agent=user_agent,
    )
    db.add(sess)
    db.commit()
    db.refresh(sess)
    return sess

def revoke_session(db: Session, sess: DbSession):
    sess.revoked_at = datetime.now(timezone.utc)
    db.add(sess)
    db.commit()

def revoke_all_sessions(db: Session, user_id: int):
    now = datetime.now(timezone.utc)
    db.query(DbSession).filter(DbSession.user_id == user_id, DbSession.revoked_at.is_(None)).update(
        {"revoked_at": now}, synchronize_session=False
    )
    db.commit()

def update_user(db: Session, user: User, full_name: str | None, email: str | None) -> User:
    if email is not None:
        email = email.lower()
        taken = db.query(User).filter(User.email == email, User.id != user.id).first()
        if taken:
            raise HTTPException(status_code=400, detail="Email уже занят")
        user.email = email

    if full_name is not None:
        user.full_name = full_name

    user.updated_at = datetime.now(timezone.utc)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def soft_delete_user(db: Session, user: User):
    user.is_active = False
    user.updated_at = datetime.now(timezone.utc)
    db.add(user)
    db.commit()
    revoke_all_sessions(db, user.id)
