from fastapi import APIRouter, Depends, Request, Response, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.config import settings
from app.core.security import create_jwt
from .schemas import RegisterIn, LoginIn, LoginOut, UserOut, UpdateMeIn
from .service import create_user, authenticate_user, create_session, revoke_session, update_user, soft_delete_user

router = APIRouter(prefix="/api/auth", tags=["auth"])

def require_user(request: Request):
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user

@router.post("/register", response_model=UserOut, status_code=201)
def register(data: RegisterIn, db: Session = Depends(get_db)):
    if data.password != data.password2:
        raise HTTPException(status_code=400, detail="Пароли не совпадают")
    user = create_user(db, data.full_name, data.email, data.password)
    return UserOut.model_validate(user, from_attributes=True)

@router.post("/login", response_model=LoginOut)
def login(data: LoginIn, request: Request, response: Response, db: Session = Depends(get_db)):
    user = authenticate_user(db, data.email, data.password)

    ip = request.headers.get("X-Forwarded-For", "").split(",")[0].strip() or request.client.host
    ua = request.headers.get("User-Agent")

    sess = create_session(db, user, ip, ua)
    token = create_jwt(uid=user.id, sid=sess.id)

    max_age = settings.session_expire_days * 24 * 60 * 60  # секунды

    response.set_cookie(
        key=settings.cookie_name,
        value=sess.id,
        httponly=True,
        secure=settings.cookie_secure,
        samesite="lax",
        max_age=max_age,
    )

    return LoginOut(user=UserOut.model_validate(user, from_attributes=True), token=token)

@router.post("/logout", status_code=204)
def logout(request: Request, response: Response, db: Session = Depends(get_db)):
    user = require_user(request)
    sess = getattr(request.state, "session", None)

    if sess:
        revoke_session(db, sess)

    response.delete_cookie(settings.cookie_name)
    return Response(status_code=204)

@router.get("/me", response_model=UserOut)
def me(request: Request):
    user = require_user(request)
    return UserOut.model_validate(user, from_attributes=True)

@router.patch("/me", response_model=UserOut)
def update_me(data: UpdateMeIn, request: Request, db: Session = Depends(get_db)):
    user = require_user(request)
    user = update_user(db, user, data.full_name, data.email)
    return UserOut.model_validate(user, from_attributes=True)

@router.delete("/me", status_code=204)
def delete_me(request: Request, response: Response, db: Session = Depends(get_db)):
    user = require_user(request)
    # soft delete + logout
    soft_delete_user(db, user)
    response.delete_cookie(settings.cookie_name)
    return Response(status_code=204)
