from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from sqlalchemy.orm import Session as OrmSession

from app.accounts.models import Session as DbSession
from app.core.config import settings
from app.core.security import decode_jwt

class AuthMiddleware(BaseHTTPMiddleware):
    """
    Ставит request.state.user и request.state.session, если пользователь определён.
    Идентификация:
      1) Authorization: Bearer <jwt> (в jwt есть uid + sid) -> проверяем сессию в БД
      2) Cookie sessionid -> проверяем сессию в БД
    """
    def __init__(self, app, db_factory):
        super().__init__(app)
        self.db_factory = db_factory

    async def dispatch(self, request: Request, call_next):
        request.state.user = None
        request.state.session = None

        db: OrmSession = self.db_factory()
        try:
            # 1) Bearer JWT
            auth = request.headers.get("Authorization", "")
            if auth.startswith("Bearer "):
                token = auth[7:].strip()
                user_session = self._auth_by_jwt(db, token)
                if user_session:
                    user, sess = user_session
                    request.state.user = user
                    request.state.session = sess
                    return await call_next(request)

            # 2) Cookie sessionid
            sid = request.cookies.get(settings.cookie_name)
            if sid:
                user_session = self._auth_by_session(db, sid)
                if user_session:
                    user, sess = user_session
                    request.state.user = user
                    request.state.session = sess
        finally:
            db.close()

        return await call_next(request)

    def _auth_by_jwt(self, db: OrmSession, token: str):
        try:
            payload = decode_jwt(token)
        except Exception:
            return None
        uid = payload.get("uid")
        sid = payload.get("sid")
        if not uid or not sid:
            return None

        sess = db.query(DbSession).filter(DbSession.id == sid, DbSession.user_id == uid).first()
        if not sess or not sess.is_valid():
            return None
        return (sess.user, sess)

    def _auth_by_session(self, db: OrmSession, sid: str):
        sess = db.query(DbSession).filter(DbSession.id == sid).first()
        if not sess or not sess.is_valid():
            return None
        return (sess.user, sess)
