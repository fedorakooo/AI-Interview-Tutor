import random

from langchain_core.prompts import ChatPromptTemplate

from src.agent.domain.models.cv_data import CVData
from src.agent.domain.models.interview_state import InterviewState
from src.agent.domain.value_objects.conversation_role import ConversationRole
from src.agent.domain.value_objects.interview_stage import IntermediateInterviewStage
from src.agent.llm import llm
from src.agent.prompts.hard_question import HARD_QUESTION_PROMPT_HUMAN, HARD_QUESTION_PROMPT_SYSTEM


def ask_hard_question_node(state: InterviewState) -> InterviewState:
    print(state["hard_question_completed"])
    print("ask_hard_question_node")

    if state["hard_questions_turns"] == 0:
        hard_greetings = [
            "Let's go to checking your hard skills.",
            "Now, let's dive into some technical questions.",
            "Great! Time to test your technical knowledge!",
            "Now we'll check your technical knowledge. Are you ready to go?",
        ]

        message = random.choice(hard_greetings)
        state["hard_questions_turns"] += 1
        state["intermediate_stage"] = IntermediateInterviewStage.QUESTION
        state["messages"].append((ConversationRole.AGENT, message))
        return state

    messages = state.get("messages", [])

    state["hard_questions_turns"] += 1

    conversation_context = "\n".join([entry[1] for entry in messages])

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", HARD_QUESTION_PROMPT_SYSTEM),
            ("human", HARD_QUESTION_PROMPT_HUMAN),
        ]
    )

    chain = prompt | llm
    generated_question = chain.invoke(
        {"conversation_context": conversation_context, "cv_summary": CVData(**state["cv_data"]).model_dump_json()}
    ).content.strip()

    messages.append((ConversationRole.AGENT, generated_question))
    state["messages"] = messages
    state["intermediate_stage"] = IntermediateInterviewStage.QUESTION

    return state
