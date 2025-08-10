from typing import TypedDict


class EducationItem(TypedDict):
    institution: str | None
    faculty: str | None
    degree: str | None
    start_year: int | None
    end_year: int | None


class ExperienceItem(TypedDict):
    company: str
    role: str
    start_date: str
    end_date: str
    responsibilities: list[str]


class LanguageItem(TypedDict):
    language: str
    proficiency: str


class CVData(TypedDict):
    user_name: str
    specialization: str | None
    education: list[EducationItem] | None
    experience: list[ExperienceItem] | None
    additional_competitive_achievements: list[str] | None
    skills: list[str] | None
    languages: list[LanguageItem] | None
