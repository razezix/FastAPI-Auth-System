from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.access.service import can
from .mock_data import PRODUCTS, ORDERS

router = APIRouter(prefix="/api", tags=["business"])

def require_user(request: Request):
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user

def filter_by_owner(items: list[dict], user_id: int):
    return [x for x in items if x.get("owner_id") == user_id]

# ---- PRODUCTS ----
@router.get("/products")
def list_products(request: Request, db: Session = Depends(get_db)):
    user = require_user(request)

    if not can(db, user.id, "products", "read", owner_id=None):
        raise HTTPException(status_code=403, detail="Forbidden")

    # если есть read_all -> вернём все, иначе только свои
    if can(db, user.id, "products", "read", owner_id=user.id + 10_000):
        return PRODUCTS
    return filter_by_owner(PRODUCTS, user.id)

@router.get("/products/{pid}")
def get_product(pid: int, request: Request, db: Session = Depends(get_db)):
    user = require_user(request)
    obj = next((x for x in PRODUCTS if x["id"] == pid), None)
    if not obj:
        raise HTTPException(404, "Not found")

    if not can(db, user.id, "products", "read", owner_id=obj["owner_id"]):
        raise HTTPException(status_code=403, detail="Forbidden")
    return obj

@router.post("/products")
def create_product(request: Request, db: Session = Depends(get_db)):
    user = require_user(request)
    if not can(db, user.id, "products", "create", owner_id=None):
        raise HTTPException(status_code=403, detail="Forbidden")
    return {"detail": "Created (mock)", "owner_id": user.id}

@router.patch("/products/{pid}")
def update_product(pid: int, request: Request, db: Session = Depends(get_db)):
    user = require_user(request)
    obj = next((x for x in PRODUCTS if x["id"] == pid), None)
    if not obj:
        raise HTTPException(404, "Not found")

    if not can(db, user.id, "products", "update", owner_id=obj["owner_id"]):
        raise HTTPException(status_code=403, detail="Forbidden")
    return {"detail": "Updated (mock)", "id": pid}

@router.delete("/products/{pid}", status_code=204)
def delete_product(pid: int, request: Request, db: Session = Depends(get_db)):
    user = require_user(request)
    obj = next((x for x in PRODUCTS if x["id"] == pid), None)
    if not obj:
        raise HTTPException(404, "Not found")

    if not can(db, user.id, "products", "delete", owner_id=obj["owner_id"]):
        raise HTTPException(status_code=403, detail="Forbidden")
    return None

# ---- ORDERS (аналогично) ----
@router.get("/orders")
def list_orders(request: Request, db: Session = Depends(get_db)):
    user = require_user(request)

    if not can(db, user.id, "orders", "read", owner_id=None):
        raise HTTPException(status_code=403, detail="Forbidden")

    if can(db, user.id, "orders", "read", owner_id=user.id + 10_000):
        return ORDERS
    return filter_by_owner(ORDERS, user.id)
