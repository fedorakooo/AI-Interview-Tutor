from langchain_core.prompts import ChatPromptTemplate

from src.agent.domain.models.interview_state import InterviewState
from src.agent.domain.value_objects.conversation_role import ConversationRole
from src.agent.llm import llm


def wrap_up_node(state: InterviewState) -> InterviewState:
    """
    Handles the wrap-up of the interview, politely saying goodbye to the candidate.
    """
    print("wrap_up_node")

    messages = state.get("messages", [])

    final_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a polite, friendly interview assistant."),
            (
                "human",
                """
                End the interview politely. Thank the candidate for their time and participation.
                Say goodbye warmly and professionally.

                Conversation context:
                {conversation_context}
                """,
            ),
        ]
    )

    conversation_context = "\n".join([entry[1] for entry in messages])

    chain = final_prompt | llm
    wrap_up_message = chain.invoke({"conversation_context": conversation_context}).content.strip()

    messages.append((ConversationRole.AGENT, wrap_up_message))
    state["messages"] = messages

    return state
