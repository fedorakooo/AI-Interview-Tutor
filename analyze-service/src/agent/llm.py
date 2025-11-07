from dotenv import load_dotenv

load_dotenv()


class LLMFactory:
    @staticmethod
    def create_google_llm():
        from langchain_google_genai import ChatGoogleGenerativeAI

        return ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0.2,
        )


llm = LLMFactory.create_google_llm()
