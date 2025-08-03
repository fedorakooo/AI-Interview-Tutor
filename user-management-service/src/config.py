from pathlib import Path
from typing import Any

import yaml
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
    """Postgres connection settings."""

    POSTGRES_USER: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_NAME: str
    POSTGRES_PASSWORD: str

    @property
    def url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_NAME}"
        )

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class SQLAlchemySettings(BaseSettings):
    """SQLAlchemy configuration settings."""

    ECHO: bool = False
    POOL_SIZE: int = 5
    MAX_OVERFLOW: int = 10
    EXPIRE_ON_COMMIT: bool = False


class LoggerSettings(BaseSettings):
    """Logging configuration settings."""

    LOGGING_CONFIG: dict[str, Any] = {}

    @classmethod
    def load_from_yaml(cls, file_path: str = "config.yaml") -> dict[str, Any]:
        """Load logging configuration from YAML file."""
        path = Path(file_path)
        if not path.exists():
            return {}

        with path.open() as f:
            config = yaml.safe_load(f)
            return config.get("logger", {})


class JWTSettings(BaseSettings):
    """JWT settings."""

    PRIVATE_KEY: str
    PUBLIC_KEY: str
    algorithm: str = "RS256"
    access_token_expire_minutes: float = 10
    refresh_token_expire_minutes: float = 20160

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @classmethod
    def load_from_yaml(cls, file_path: str = "config.yaml") -> dict[str, Any]:
        """Load JWT configuration from YAML file."""
        path = Path(__file__).parent.parent / file_path
        if not path.exists():
            return {}

        with path.open() as f:
            config = yaml.safe_load(f)
            return config.get("jwt_handler", {})


class Settings(BaseSettings):
    """Application settings container."""

    postgres_settings: PostgresSettings = PostgresSettings()
    sql_alchemy_settings: SQLAlchemySettings = SQLAlchemySettings()
    logger_settings: LoggerSettings = LoggerSettings()
    jwt_settings: JWTSettings = JWTSettings()

    def __init__(self) -> None:
        super().__init__()
        self.logger_settings.LOGGING_CONFIG = LoggerSettings.load_from_yaml()
        jwt_config = JWTSettings.load_from_yaml()
        self.jwt_settings = JWTSettings(**jwt_config)


settings = Settings()
