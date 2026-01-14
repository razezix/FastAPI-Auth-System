from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    database_url: str = Field(alias="DATABASE_URL")
    secret_key: str = Field(default="change-me", alias="SECRET_KEY")

    jwt_expire_minutes: int = Field(default=60, alias="JWT_EXPIRE_MINUTES")
    session_expire_days: int = Field(default=7, alias="SESSION_EXPIRE_DAYS")

    cookie_name: str = Field(default="sessionid", alias="COOKIE_NAME")
    cookie_secure: bool = Field(default=False, alias="COOKIE_SECURE")

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
