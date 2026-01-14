from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.access.models import Role, Resource, AccessRule
from app.access.schemas import RoleIn, RoleOut, ResourceIn, ResourceOut, AccessRuleIn, AccessRuleOut
from app.access.service import require_admin

router = APIRouter(prefix="/api/admin", tags=["admin"])

def require_user_id(request: Request) -> int:
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user.id

# ---- Roles ----
@router.get("/roles", response_model=list[RoleOut])
def list_roles(request: Request, db: Session = Depends(get_db)):
    uid = require_user_id(request)
    require_admin(db, uid)
    roles = db.query(Role).order_by(Role.id).all()
    return [RoleOut.model_validate(r, from_attributes=True) for r in roles]

@router.post("/roles", response_model=RoleOut, status_code=201)
def create_role(data: RoleIn, request: Request, db: Session = Depends(get_db)):
    uid = require_user_id(request)
    require_admin(db, uid)
    if db.query(Role).filter(Role.name == data.name).first():
        raise HTTPException(400, "Role already exists")
    role = Role(name=data.name, description=data.description)
    db.add(role); db.commit(); db.refresh(role)
    return RoleOut.model_validate(role, from_attributes=True)

@router.patch("/roles/{role_id}", response_model=RoleOut)
def update_role(role_id: int, data: RoleIn, request: Request, db: Session = Depends(get_db)):
    uid = require_user_id(request)
    require_admin(db, uid)
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(404, "Not found")
    role.name = data.name
    role.description = data.description
    db.add(role); db.commit(); db.refresh(role)
    return RoleOut.model_validate(role, from_attributes=True)

@router.delete("/roles/{role_id}", status_code=204)
def delete_role(role_id: int, request: Request, db: Session = Depends(get_db)):
    uid = require_user_id(request)
    require_admin(db, uid)
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(404, "Not found")
    db.delete(role); db.commit()
    return None

# ---- Resources ----
@router.get("/resources", response_model=list[ResourceOut])
def list_resources(request: Request, db: Session = Depends(get_db)):
    uid = require_user_id(request)
    require_admin(db, uid)
    items = db.query(Resource).order_by(Resource.id).all()
    return [ResourceOut.model_validate(r, from_attributes=True) for r in items]

@router.post("/resources", response_model=ResourceOut, status_code=201)
def create_resource(data: ResourceIn, request: Request, db: Session = Depends(get_db)):
    uid = require_user_id(request)
    require_admin(db, uid)
    if db.query(Resource).filter(Resource.code == data.code).first():
        raise HTTPException(400, "Resource already exists")
    res = Resource(code=data.code, description=data.description)
    db.add(res); db.commit(); db.refresh(res)
    return ResourceOut.model_validate(res, from_attributes=True)

@router.patch("/resources/{resource_id}", response_model=ResourceOut)
def update_resource(resource_id: int, data: ResourceIn, request: Request, db: Session = Depends(get_db)):
    uid = require_user_id(request)
    require_admin(db, uid)
    res = db.query(Resource).filter(Resource.id == resource_id).first()
    if not res:
        raise HTTPException(404, "Not found")
    res.code = data.code
    res.description = data.description
    db.add(res); db.commit(); db.refresh(res)
    return ResourceOut.model_validate(res, from_attributes=True)

@router.delete("/resources/{resource_id}", status_code=204)
def delete_resource(resource_id: int, request: Request, db: Session = Depends(get_db)):
    uid = require_user_id(request)
    require_admin(db, uid)
    res = db.query(Resource).filter(Resource.id == resource_id).first()
    if not res:
        raise HTTPException(404, "Not found")
    db.delete(res); db.commit()
    return None

# ---- Access Rules ----
@router.get("/access-rules", response_model=list[AccessRuleOut])
def list_rules(request: Request, db: Session = Depends(get_db)):
    uid = require_user_id(request)
    require_admin(db, uid)
    rules = db.query(AccessRule).order_by(AccessRule.id).all()
    return [AccessRuleOut.model_validate(r, from_attributes=True) for r in rules]

@router.post("/access-rules", response_model=AccessRuleOut, status_code=201)
def create_rule(data: AccessRuleIn, request: Request, db: Session = Depends(get_db)):
    uid = require_user_id(request)
    require_admin(db, uid)
    rule = AccessRule(**data.model_dump())
    db.add(rule); db.commit(); db.refresh(rule)
    return AccessRuleOut.model_validate(rule, from_attributes=True)

@router.patch("/access-rules/{rule_id}", response_model=AccessRuleOut)
def update_rule(rule_id: int, data: AccessRuleIn, request: Request, db: Session = Depends(get_db)):
    uid = require_user_id(request)
    require_admin(db, uid)
    rule = db.query(AccessRule).filter(AccessRule.id == rule_id).first()
    if not rule:
        raise HTTPException(404, "Not found")
    for k, v in data.model_dump().items():
        setattr(rule, k, v)
    db.add(rule); db.commit(); db.refresh(rule)
    return AccessRuleOut.model_validate(rule, from_attributes=True)

@router.delete("/access-rules/{rule_id}", status_code=204)
def delete_rule(rule_id: int, request: Request, db: Session = Depends(get_db)):
    uid = require_user_id(request)
    require_admin(db, uid)
    rule = db.query(AccessRule).filter(AccessRule.id == rule_id).first()
    if not rule:
        raise HTTPException(404, "Not found")
    db.delete(rule); db.commit()
    return None
