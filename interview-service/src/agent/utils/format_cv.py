from src.agent.domain.models.cv_data import CVData


def format_cv(cv_data: CVData) -> str:
    lines = []

    lines.append(f"Name: {cv_data.get('user_name', 'N/A')}")
    if cv_data.get("specialization"):
        lines.append(f"Specialization: {cv_data['specialization']}")

    education_list = cv_data.get("education") or []
    if education_list:
        lines.append("Education:")
        for edu in education_list:
            inst = edu.get("institution") or "N/A"
            faculty = edu.get("faculty") or "N/A"
            degree = edu.get("degree") or "N/A"
            start = edu.get("start_year") or "N/A"
            end = edu.get("end_year") or "N/A"
            lines.append(f"  - {degree} in {faculty}, {inst} ({start}–{end})")

    # Experience
    experience_list = cv_data.get("experience") or []
    if experience_list:
        lines.append("Experience:")
        for exp in experience_list:
            company = exp.get("company", "N/A")
            role = exp.get("role", "N/A")
            start = exp.get("start_date", "N/A")
            end = exp.get("end_date", "N/A")
            lines.append(f"  - {role} at {company} ({start}–{end})")
            for r in exp.get("responsibilities") or []:
                lines.append(f"    * {r}")

    # Skills
    skills_list = cv_data.get("skills") or []
    if skills_list:
        lines.append("Skills: " + ", ".join(skills_list))

    # Languages
    languages_list = cv_data.get("languages") or []
    if languages_list:
        lines.append("Languages:")
        for lang in languages_list:
            language = lang.get("language", "N/A")
            prof = lang.get("proficiency", "N/A")
            lines.append(f"  - {language}: {prof}")

    # Additional achievements
    achievements_list = cv_data.get("additional_competitive_non_work_achievements") or []
    if achievements_list:
        lines.append("Additional achievements:")
        for ach in achievements_list:
            lines.append(f"  - {ach}")

    return "\n".join(lines)
