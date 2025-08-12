from src.agent.domain.models.interview_state import InterviewState
from src.agent.domain.value_objects.conversation_role import ConversationRole
from src.agent.domain.value_objects.interview_stage import InterviewStage


def start_interview(state: InterviewState) -> InterviewState:
    greeting = "Hello! I'm your AI technical interviewer. Let's start!"
    return {**state, "interview_log": [(ConversationRole.AGENT, greeting)], "stage": InterviewStage.SOFT_QUESTIONS}
