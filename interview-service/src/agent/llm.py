from dotenv import load_dotenv

from src.agent.config import settings

load_dotenv()


class LLMFactory:
    @staticmethod
    def create_google_llm():
        from langchain_google_genai import ChatGoogleGenerativeAI

        return ChatGoogleGenerativeAI(
            model=settings.google_llm.model,
            temperature=settings.google_llm.temperature,
        )

    @staticmethod
    def create_custom_llm():
        from langchain_openai import ChatOpenAI

        cfg = settings.custom_llm
        return ChatOpenAI(
            openai_api_base=cfg.api_base,
            openai_api_key=cfg.api_key,
            model=cfg.model,
            temperature=cfg.temperature,
        )


llm = LLMFactory.create_google_llm()
