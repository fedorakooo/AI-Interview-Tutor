from langchain_openai import ChatOpenAI

from src.config import settings


def initialize_llm() -> ChatOpenAI:
    return ChatOpenAI(
        openai_api_base=settings.llm_config.api_base,
        openai_api_key=settings.llm_config.api_key,
        model=settings.llm_config.model,
        temperature=settings.llm_config.temperature,
    )


llm = initialize_llm()
