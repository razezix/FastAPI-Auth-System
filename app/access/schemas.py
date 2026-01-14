from pydantic import BaseModel, Field

class RoleIn(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    description: str = ""

class RoleOut(RoleIn):
    id: int

class ResourceIn(BaseModel):
    code: str = Field(min_length=1, max_length=80)
    description: str = ""

class ResourceOut(ResourceIn):
    id: int

class AccessRuleIn(BaseModel):
    role_id: int
    resource_id: int

    read_permission: bool = False
    read_all_permission: bool = False
    create_permission: bool = False
    update_permission: bool = False
    update_all_permission: bool = False
    delete_permission: bool = False
    delete_all_permission: bool = False

class AccessRuleOut(AccessRuleIn):
    id: int
