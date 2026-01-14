from pydantic import BaseModel, EmailStr, Field

class RegisterIn(BaseModel):
    full_name: str = Field(min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(min_length=6)
    password2: str = Field(min_length=6)

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    is_active: bool

class UpdateMeIn(BaseModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = None

class LoginOut(BaseModel):
    user: UserOut
    token: str
