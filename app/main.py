from fastapi import FastAPI
from app.core.database import engine, Base, SessionLocal
from app.core.auth_middleware import AuthMiddleware

from app.accounts.router import router as auth_router
from app.access.router import router as admin_router
from app.business.router import router as business_router

from app.access.seed import seed_if_empty

app = FastAPI(title="Custom Auth/AuthZ (FastAPI)")

# Middleware должен иметь доступ к БД -> передаём фабрику сессий
app.add_middleware(AuthMiddleware, db_factory=SessionLocal)

@app.on_event("startup")
def on_startup():
    # для демо можно создать таблицы автоматически
    Base.metadata.create_all(bind=engine)

    # сидирование тестовых данных
    db = SessionLocal()
    try:
        seed_if_empty(db)
    finally:
        db.close()

app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(business_router)
