import os
from typing import Any, Dict, Optional

from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    PROJECT_NAME: str = "TestApp"

    POSTGRES_SERVER: Optional[str] = os.environ.get("POSTGRES_SERVER")
    POSTGRES_USER: Optional[str] = os.environ.get("POSTGRES_USER")
    POSTGRES_PASSWORD: Optional[str] = os.environ.get("POSTGRES_PASSWORD")
    POSTGRES_DB: Optional[str] = os.environ.get("POSTGRES_DB")
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER") or "localhost",
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    UVICORN_HOST: Optional[str] = os.environ.get("UVICORN_HOST")
    UVICORN_PORT: Optional[int] = os.environ.get("UVICORN_PORT")
    UVICORN_WORKERS: Optional[int] = os.environ.get("UVICORN_WORKERS")
    DEV_MODE: bool = True if os.environ.get("MODE") == "DEV" else False

    EMAIL_TEST_USER: str = "test@example.com"
    FIRST_SUPERUSER: Optional[str] = os.environ.get("FIRST_SUPERUSER")
    FIRST_SUPERUSER_PASSWORD: Optional[str] = os.environ.get("FIRST_SUPERUSER_PASSWORD")

    class Config:
        case_sensitive = True


settings = Settings()
