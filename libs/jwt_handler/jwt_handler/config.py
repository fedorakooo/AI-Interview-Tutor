from pathlib import Path
from typing import Any

import yaml
from pydantic_settings import BaseSettings, SettingsConfigDict


class JWTSettings(BaseSettings):
    """JWT settings."""

    PRIVATE_KEY: str
    PUBLIC_KEY: str
    algorithm: str = "RS256"
    access_token_expire_minutes: float = 10
    refresh_token_expire_minutes: float = 20160

    model_config = SettingsConfigDict(env_file="../.env", extra="ignore")

    @classmethod
    def load_from_yaml(cls, file_path: str = "config.yaml") -> dict[str, Any]:
        """Load JWT configuration from YAML file."""
        path = Path(__file__).parent / file_path
        if not path.exists():
            return {}

        with path.open() as f:
            config = yaml.safe_load(f)
            return config.get("jwt_handler", {})


settings = JWTSettings()
settings.load_from_yaml()
