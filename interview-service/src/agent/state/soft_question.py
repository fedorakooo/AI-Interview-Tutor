import json

from langchain_core.prompts import ChatPromptTemplate

from src.agent.domain.models.interview_state import InterviewState
from src.agent.domain.value_objects.conversation_role import ConversationRole
from src.agent.domain.value_objects.interview_stage import IntermediateInterviewStage
from src.agent.llm import llm
from src.agent.utils.format_messages import format_messages


def ask_soft_question_node(state: InterviewState) -> InterviewState:
    print("ask_soft_question_node")

    messages = state["messages"]
    cv_data = state["cv_data"]

    state["soft_questions_turns"] += 1

    conversation_context = format_messages(messages)

    final_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a polite and tactful interview assistant."),
            (
                "human",
                """
                Generate ONE soft, non-technical question for a candidate.
                Focus on behavioral, interpersonal, or work-style topics.
                Make it natural, warm, and respectful.
                Avoid repeating questions that have already been asked.

                Interview context:
                {conversation_context}

                Candidate CV:
                {cv_summary}
                """,
            ),
        ]
    )

    chain = final_prompt | llm

    generated_question = chain.invoke(
        {
            "conversation_context": conversation_context,
            "cv_summary": json.dumps(cv_data, indent=2),
        }
    ).content.strip()

    messages.append((ConversationRole.AGENT, generated_question))

    state["messages"] = messages
    state["intermediate_stage"] = IntermediateInterviewStage.QUESTION

    return state
