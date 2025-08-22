from langchain_core.prompts import ChatPromptTemplate

from src.agent.domain.models.interview_state import InterviewState
from src.agent.domain.value_objects.conversation_role import ConversationRole
from src.agent.llm import llm
from src.agent.utils.format_messages import format_messages


def small_talk_node(state: InterviewState) -> InterviewState:
    print("small_talk_node")

    messages = state["messages"]

    conversation_context = format_messages(messages)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a polite, friendly assistant who engages in natural, clean small talk."),
            (
                "human",
                """
                Continue a polite and friendly conversation with the candidate.

                Important:
                - Keep the conversation clean and professional.
                - Be warm and natural.
                - Avoid interview or technical questions unless prompted.
                - Respond to the user's input only.

                Interview context:
                {conversation_context}

                Your message should be based on the last user message
                """,
            ),
        ]
    )

    chain = prompt | llm

    assistant_reply = chain.invoke({"conversation_context": conversation_context}).content.strip()

    messages.append((ConversationRole.AGENT, assistant_reply))
    state["messages"] = messages

    return state
