from pathlib import Path
from typing import Any

import yaml
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent
SOFT_QUESTIONS_JSON_PATH = BASE_DIR / "data" / "soft_questions.json"


class LLMConfig(BaseSettings):
    model: str
    temperature: float = 0.6
    api_base: str | None = None
    api_key: str | None = None


class LoggerSettings(BaseSettings):
    """Logging configuration settings."""

    logging_config: dict[str, Any] = {}

    @classmethod
    def load_from_yaml(cls, file_path: str = "config.yaml") -> dict[str, Any]:
        """Load logging configuration from YAML file."""
        path = Path(file_path)
        if not path.exists():
            return {}

        with path.open() as f:
            config = yaml.safe_load(f)
            return config.get("logger", {})


class Settings(BaseSettings):
    logger_settings: LoggerSettings = LoggerSettings()
    google_llm: LLMConfig = LLMConfig(model="gemini-2.0-flash")
    custom_llm: LLMConfig = LLMConfig(
        model="ai/gemma3",
        api_base="http://localhost:12434/engines/v1",
        api_key="ignored",
    )

    def __init__(self) -> None:
        super().__init__()
        self.logger_settings.logging_config = LoggerSettings.load_from_yaml()


settings = Settings()
