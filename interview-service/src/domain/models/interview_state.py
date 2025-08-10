from typing import TypedDict

from src.domain.models.cv_data import CVData
from src.domain.models.user_profile import UserProfile
from src.domain.value_objects.conversation_role import ConversationRole
from src.domain.value_objects.interview_stage import InterviewStage


class InterviewState(TypedDict):
    developer_profile: UserProfile
    interview_log: list[tuple[ConversationRole, str]]
    cv_data: CVData
    stage: InterviewStage
    self_intro: str
    self_intro_turns: int
    soft_questions_turns: int
    soft_skill_questions: list[str]
    user_answer: str
    missing_fields: list[str]
