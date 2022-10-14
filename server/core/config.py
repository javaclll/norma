import os
from typing import Any, Dict, List, Optional

import yaml
from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    PROJECT_NAME: str = "TestApp"
    DEV_MODE: bool

    ENGINE_IDENT: str

    POSTGRES_SERVER: Optional[str]
    POSTGRES_USER: Optional[str]
    POSTGRES_PASSWORD: Optional[str]
    POSTGRES_DB: Optional[str]
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn]

    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_PASSWORD: str

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl]

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

    UVICORN_HOST: Optional[str]
    UVICORN_PORT: Optional[int]
    UVICORN_WORKERS: Optional[int]

    FIRST_SUPERUSER: Optional[str]
    FIRST_SUPERUSER_PASSWORD: Optional[str]

    class Config:
        case_sensitive = True


configs = {}

with open("etc/base.yml", "r") as base_config_file:
    configs = yaml.load(base_config_file.read(), yaml.Loader)

config_path = os.environ.get("CONFIG_PATH") or "etc/dev.yml"

with open(config_path, "r") as config_file:
    custom_configs = yaml.load(config_file.read(), yaml.Loader)
    configs.update(custom_configs)

settings = Settings(**configs)
