from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import END
from langgraph.graph import StateGraph

from src.agent.state import handle_self_introduction
from src.domain.models.interview_state import InterviewState
from src.domain.value_objects.conversation_role import ConversationRole
from src.domain.value_objects.interview_stage import InterviewStage


def create_interview_workflow():
    def start_interview(state: InterviewState) -> InterviewState:
        greeting = "Hello! I'm your AI technical interviewer. Let's start!"
        return {**state, "interview_log": [(ConversationRole.AGENT, greeting)], "stage": InterviewStage.SELF_INTRO}

    workflow = StateGraph(InterviewState)

    # Add nodes
    workflow.add_node("start_interview", start_interview)
    workflow.add_node("handle_self_introduction", handle_self_introduction)

    # Define routing
    def route_based_on_stage(state: InterviewState) -> str:
        if not state.get("interview_log"):
            return "start_interview"

        if state["stage"] == "Self Intro":
            return "handle_self_introduction"

        return END

    # Configure workflow
    workflow.set_conditional_entry_point(
        route_based_on_stage,
        {
            "start_interview": "start_interview",
            "handle_self_introduction": "handle_self_introduction",
            "__end__": END,
        },
    )

    workflow.add_edge("start_interview", "handle_self_introduction")
    workflow.add_conditional_edges(
        "handle_self_introduction",
        route_based_on_stage,
        {
            "handle_self_introduction": "handle_self_introduction",
            "__end__": END,
        },
    )

    return workflow.compile(checkpointer=MemorySaver())
