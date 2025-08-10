from langchain_core.prompts import ChatPromptTemplate

from src.agent.llm import llm
from src.agent.utils import format_conversation_history
from src.config import settings
from src.domain.models.interview_state import InterviewState
from src.domain.value_objects.conversation_role import ConversationRole
from src.domain.value_objects.interview_stage import InterviewStage


def generate_missing_field_question(missing_fields: list[str], history: str) -> str | None:
    prompt_template = ChatPromptTemplate.from_template(
        """
    As an AI interviewer, generate a natural question to collect missing CV information.
    Focus on the most important missing field and maintain conversational flow.

    Missing fields: {missing_fields}
    Conversation history:
    {history}

    Respond EXACTLY in this format:
    Missing field: [field_name]
    Question: [your_question]
    """
    )

    chain = prompt_template | llm
    response = chain.invoke({"missing_fields": ", ".join(missing_fields), "history": history}).content

    field, question = None, None
    for line in response.split("\n"):
        if line.startswith("Missing field:"):
            field = line.split(":", 1)[1].strip()
        elif line.startswith("Question:"):
            question = line.split(":", 1)[1].strip()

    return question if field and question else None


def handle_self_introduction(state: InterviewState) -> InterviewState:
    log = state["interview_log"]

    if log and log[-1][0] == ConversationRole.USER:
        state["self_intro"] += log[-1][1] + " "

    # Check exit conditions
    if not state["missing_fields"] or state["self_intro_turns"] >= settings.agent_settings.max_self_intro_turns:
        state["stage"] = InterviewStage.SOFT_QUESTIONS
        return state

    # Generate next question
    question = generate_missing_field_question(
        missing_fields=state["missing_fields"], history=format_conversation_history(log)
    )

    if question:
        state["interview_log"].append((ConversationRole.AGENT, question))
        state["self_intro_turns"] += 1
    else:
        state["stage"] = InterviewStage.SOFT_QUESTIONS

    return state
