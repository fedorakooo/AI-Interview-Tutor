from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import END
from langgraph.graph import StateGraph

from src.agent.domain.models.interview_state import InterviewState
from src.agent.domain.value_objects.interview_stage import InterviewStage
from src.agent.state.soft_questions import ask_soft_questions
from src.agent.state.start_interview import start_interview


def create_interview_workflow():

    workflow = StateGraph(InterviewState)

    workflow.add_node("start_interview", start_interview)
    workflow.add_node("ask_soft_questions", ask_soft_questions)

    # Define routing
    def route_based_on_stage(state: InterviewState) -> str:
        if not state.get("interview_log"):
            return "start_interview"

        if state["stage"] == InterviewStage.GREETING:
            return "start_interview"

        if state["stage"] == InterviewStage.SOFT_QUESTIONS:
            if state.get("interview_log") and state["interview_log"][-1][0] == "Agent":
                return END
            return "ask_soft_questions"

        return END

    # Configure workflow
    workflow.set_conditional_entry_point(
        route_based_on_stage,
        {
            "start_interview": "start_interview",
            "ask_soft_questions": "ask_soft_questions",
            "__end__": END,
        },
    )

    workflow.add_edge("start_interview", "ask_soft_questions")
    workflow.add_conditional_edges(
        "ask_soft_questions",
        route_based_on_stage,
        {
            "ask_soft_questions": "ask_soft_questions",
            "__end__": END,
        },
    )

    return workflow.compile(checkpointer=MemorySaver())
