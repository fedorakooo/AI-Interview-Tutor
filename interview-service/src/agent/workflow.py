import json

from langchain_core.prompts import ChatPromptTemplate
from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import END
from langgraph.graph import StateGraph

from src.agent.domain.models.interview_state import InterviewState
from src.agent.domain.value_objects.interview_stage import IntermediateInterviewStage, OverallInterviewStage
from src.agent.llm import llm
from src.agent.state.evaluate_answer import evaluate_answer_node
from src.agent.state.greeting import greeting_node
from src.agent.state.hard_question import ask_hard_question_node
from src.agent.state.question_router import question_router_node
from src.agent.state.small_talk import small_talk_node
from src.agent.state.soft_question import ask_soft_question_node
from src.agent.state.wrap_up import wrap_up_node
from src.agent.utils.format_messages import format_messages


def section_router(state: InterviewState) -> str:
    print("section_router")
    print(state["overall_stage"])

    if state["overall_stage"] == OverallInterviewStage.WRAP_UP:
        print("wrap_up")
        return "wrap_up"

    if state["intermediate_stage"] == IntermediateInterviewStage.QUESTION:
        return "evaluate_answer"

    if state["overall_stage"] == OverallInterviewStage.GREETING:
        return "greeting"

    if state["overall_stage"] in {
        OverallInterviewStage.SOFT_QUESTIONS,
        OverallInterviewStage.HARD_QUESTIONS,
    }:
        return "question_router"

    return END


def question_router_decision(state: InterviewState) -> str:
    print("question_router_decision")

    stage = state.get("overall_stage")

    decision_prompt = ChatPromptTemplate.from_template(
        """
        You are an exceptionally polite and tactful interview assistant.
        Your role is to maintain a warm, professional, and respectful tone at all times.

        Based on the conversation so far and candidate's CV,
        decide whether to:
        - continue with a short, friendly small talk phrase, OR
        - politely move forward by asking the next interview question.

        You MUST return ONLY one of the following words (in uppercase, without quotes or punctuation):
        SMALLTALK
        QUESTION

        ---
        Conversation context:
        {conversation_context}

        Candidate CV:
        {cv_summary}

        Your choice:
        """
    )

    chain = decision_prompt | llm
    decision = (
        chain.invoke(
            {
                "conversation_context": format_messages(state.get("messages", [])),
                "cv_summary": json.dumps(state.get("cv_data", {}), indent=2),
            }
        )
        .content.strip()
        .upper()
    )

    print(decision)
    print(stage)

    if decision == "SMALLTALK":
        return "small_talk"

    if stage == OverallInterviewStage.SOFT_QUESTIONS:
        return "ask_soft_question"

    if stage == OverallInterviewStage.HARD_QUESTIONS:
        return "ask_hard_question"

    return "small_talk"


def create_interview_workflow():
    graph_builder = StateGraph(InterviewState)

    graph_builder.add_node("greeting", greeting_node)
    graph_builder.add_node("ask_soft_question", ask_soft_question_node)
    graph_builder.add_node("ask_hard_question", ask_hard_question_node)
    graph_builder.add_node("small_talk", small_talk_node)
    graph_builder.add_node("wrap_up", wrap_up_node)
    graph_builder.add_node("question_router", question_router_node)
    graph_builder.add_node("evaluate_answer", evaluate_answer_node)

    graph_builder.add_conditional_edges(
        "__start__",
        section_router,
        {
            "greeting": "greeting",
            "question_router": "question_router",
            "wrap_up": "wrap_up",
            "evaluate_answer": "evaluate_answer",
        },
    )

    graph_builder.add_conditional_edges(
        "question_router",
        question_router_decision,
        {
            "ask_soft_question": "ask_soft_question",
            "ask_hard_question": "ask_hard_question",
            "small_talk": "small_talk",
            "wrap_up": "wrap_up",
        },
    )

    graph_builder.add_edge("evaluate_answer", "question_router")
    graph_builder.add_edge("greeting", "__end__")
    graph_builder.add_edge("ask_hard_question", "__end__")
    graph_builder.add_edge("small_talk", "__end__")
    graph_builder.add_edge("wrap_up", "__end__")
    graph_builder.add_edge("ask_soft_question", "__end__")

    graph = graph_builder.compile(checkpointer=MemorySaver())

    img = graph.get_graph().draw_mermaid_png()
    with open("interview_workflow_soft_hard_smalltalk.png", "wb") as f:
        f.write(img)

    return graph
