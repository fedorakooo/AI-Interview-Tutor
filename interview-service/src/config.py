from pydantic import Field
from pydantic_settings import BaseSettings


class LLMConfig(BaseSettings):
    api_base: str = Field(default="http://localhost:12434/engines/v1")
    api_key: str = Field(default="ignored")
    model: str = Field(default="ai/gemma3")
    temperature: float = Field(default=0.6)


class AgentSettings(BaseSettings):
    max_self_intro_turns: int = Field(default=5)


class Settings(BaseSettings):
    llm_config: LLMConfig = LLMConfig()
    agent_settings: AgentSettings = AgentSettings()


settings = Settings()
