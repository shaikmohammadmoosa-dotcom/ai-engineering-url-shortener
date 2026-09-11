import os
from typing import Any, Dict
import yaml
from pydantic import BaseModel


class AppConfig(BaseModel):
    name: str
    version: str
    environment: str
    base_url: str


class ServerConfig(BaseModel):
    host: str
    port: int


class DatabaseConfig(BaseModel):
    sqlite_url: str
    redis_host: str
    redis_port: int
    redis_db: int


class ShortenerConfig(BaseModel):
    default_ttl_days: int
    code_length: int


class RateLimitConfig(BaseModel):
    requests_per_minute: int


class Settings(BaseModel):
    app: AppConfig
    server: ServerConfig
    database: DatabaseConfig
    shortener: ShortenerConfig
    rate_limit: RateLimitConfig


def load_settings(config_path: str = "config/config.yaml") -> Settings:
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found at {config_path}")

    with open(config_path, "r") as f:
        config_data: Dict[str, Any] = yaml.safe_load(f)

    return Settings(**config_data)


settings = load_settings()