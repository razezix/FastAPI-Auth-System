from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.access.models import UserRole, AccessRule, Resource, Role

ACTIONS = {"read", "create", "update", "delete"}

def is_admin(db: Session, user_id: int) -> bool:
    return (
        db.query(UserRole)
        .join(Role, Role.id == UserRole.role_id)
        .filter(UserRole.user_id == user_id, Role.name == "admin")
        .first()
        is not None
    )

def can(db: Session, user_id: int, resource_code: str, action: str, owner_id: int | None) -> bool:
    """
    owner_id:
      - None для list/create (где нет конкретного объекта)
      - конкретный owner_id для retrieve/update/delete
    """
    if action not in ACTIONS:
        return False

    resource = db.query(Resource).filter(Resource.code == resource_code).first()
    if not resource:
        return False

    role_ids = [r[0] for r in db.query(UserRole.role_id).filter(UserRole.user_id == user_id).all()]
    if not role_ids:
        return False

    rules = db.query(AccessRule).filter(AccessRule.role_id.in_(role_ids), AccessRule.resource_id == resource.id).all()
    if not rules:
        return False

    if action == "create":
        return any(r.create_permission for r in rules)

    if action == "read":
        if any(r.read_all_permission for r in rules):
            return True
        # list: owner_id None -> можно, если есть read_permission (но отдавать будем только свои)
        if owner_id is None:
            return any(r.read_permission for r in rules)
        return owner_id == user_id and any(r.read_permission for r in rules)

    if action == "update":
        if any(r.update_all_permission for r in rules):
            return True
        return owner_id == user_id and any(r.update_permission for r in rules)

    if action == "delete":
        if any(r.delete_all_permission for r in rules):
            return True
        return owner_id == user_id and any(r.delete_permission for r in rules)

    return False

def require_admin(db: Session, user_id: int):
    if not is_admin(db, user_id):
        raise HTTPException(status_code=403, detail="Forbidden")
