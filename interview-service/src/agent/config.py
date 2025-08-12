from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent
SOFT_QUESTIONS_JSON_PATH = BASE_DIR / "data" / "soft_questions.json"


class LLMConfig(BaseSettings):
    model: str
    temperature: float = 0.6
    api_base: str | None = None
    api_key: str | None = None


class Settings(BaseSettings):
    google_llm: LLMConfig = LLMConfig(model="gemini-2.0-flash")
    custom_llm: LLMConfig = LLMConfig(
        model="ai/gemma3",
        api_base="http://localhost:12434/engines/v1",
        api_key="ignored",
    )


settings = Settings()
