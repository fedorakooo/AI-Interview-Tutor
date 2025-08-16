from langchain_core.prompts import ChatPromptTemplate

from src.agent.domain.models.interview_state import InterviewState
from src.agent.llm import llm
from src.agent.prompts.evaluate_answer import EVALUATE_ANSWER_PROMPT
from src.agent.utils.format_cv import format_cv


def evaluate_answer_node(state: InterviewState) -> InterviewState:
    prompt = ChatPromptTemplate.from_template(EVALUATE_ANSWER_PROMPT)

    chain = prompt | llm

    response = (
        chain.invoke(
            {
                "question": state["messages"][-2][1],
                "answer": state["messages"][-1][1],
                "cv_context": format_cv(state["cv_data"]),
            }
        )
        .content.strip()
        .lower()
    )

    is_answer_complete = response == "complete"

    return {**state, "is_answer_complete": is_answer_complete}
