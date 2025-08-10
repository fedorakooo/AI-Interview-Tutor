from src.domain.models.cv_data import CVData


def get_missing_cv_fields(cv_data: CVData) -> list[str]:
    return [field for field, value in cv_data.items() if value is None or (isinstance(value, list) and not value)]


def format_conversation_history(log: list) -> str:
    return "\n".join(f"{role}: {msg}" for role, msg in log)
