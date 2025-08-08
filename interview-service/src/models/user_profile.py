from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field

from src.domain.value_objects.skills import BackendTechSkill

LevelInt = Annotated[int, Field(ge=1, le=10)]


class UserProfile(BaseModel):
    user_id: UUID
    backend_tech_skills: dict[BackendTechSkill, LevelInt]
