from typing import Any, TypedDict

from src.agent.domain.models.user_profile import UserProfile
from src.agent.domain.value_objects.conversation_role import ConversationRole
from src.agent.domain.value_objects.interview_stage import IntermediateInterviewStage, OverallInterviewStage


class InterviewState(TypedDict):
    user_profile: UserProfile
    messages: list[tuple[ConversationRole, str]]
    cv_data: dict[str, Any]

    overall_stage: OverallInterviewStage
    intermediate_stage: IntermediateInterviewStage

    is_answer_complete: bool

    soft_questions_turns: int
    soft_question_completed: int

    hard_questions_turns: int
    hard_question_completed: int
