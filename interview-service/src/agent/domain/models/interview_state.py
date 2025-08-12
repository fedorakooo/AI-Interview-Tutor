from typing import TypedDict

from src.agent.domain.models.cv_data import CVData
from src.agent.domain.models.user_profile import UserProfile
from src.agent.domain.value_objects.conversation_role import ConversationRole
from src.agent.domain.value_objects.interview_stage import InterviewStage


class InterviewState(TypedDict):
    developer_profile: UserProfile

    interview_log: list[tuple[ConversationRole, str]]

    cv_data: CVData

    stage: InterviewStage

    soft_questions_turns: int

    soft_questions: list[str]
