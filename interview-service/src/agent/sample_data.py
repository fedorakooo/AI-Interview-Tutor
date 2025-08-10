from src.domain.models.cv_data import CVData

SAMPLE_CV: CVData = {
    "user_name": "Aliaksandr Fedaraka",
    "specialization": "Python Developer",
    "education": [
        {
            "institution": "Belarusian State University of Informatics and Radioelectronics",
            "faculty": "Faculty of Computer Systems and Networks",
            "degree": "Bachelor of Science",
            "start_year": 2023,
            "end_year": 2027,
        },
    ],
    "experience": [
        {
            "company": "Innowise Group",
            "role": "Python Developer",
            "start_date": "April 2025",
            "end_date": "Present",
            "responsibilities": [
                "Developing and maintaining web applications using FastAPI.",
                "Developing and maintaining web applications using Django.",
            ],
        }
    ],
    "languages": [{"language": "Russian", "proficiency": "NATIVE"}, {"language": "English", "proficiency": "B1"}],
    "skills": [
        "Python",
        "C++",
        "FastAPI",
        "Django",
        "DRF",
        "SQL",
        "Redis",
        "MongoDB",
        "Kafka",
        "RabbitMQ",
        "Git",
        "Docker",
        "Kubernetes",
        "CI/CD",
        "AWS",
    ],
    "additional_competitive_achievements": None,  # Will be added during the conversation
}
