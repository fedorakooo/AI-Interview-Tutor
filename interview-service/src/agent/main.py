import uuid

from langgraph.constants import END

from src.agent.sample_data import SAMPLE_CV
from src.agent.utils import get_missing_cv_fields
from src.agent.workflow import create_interview_workflow
from src.domain.models.interview_state import InterviewState
from src.domain.models.user_profile import UserProfile
from src.domain.value_objects.interview_stage import InterviewStage


def run_interview(profile: UserProfile):
    print("--- Starting Interview ---")

    interviewer = create_interview_workflow()
    thread_id = str(uuid.uuid4())

    # Prepare initial state
    initial_state: InterviewState = {
        "developer_profile": profile,
        "interview_log": [],
        "self_intro_turns": 0,
        "self_intro": "",
        "stage": InterviewStage.GREETING,
        "cv_data": SAMPLE_CV,
        "missing_fields": get_missing_cv_fields(SAMPLE_CV),
        "soft_questions_turns": 0,
        "soft_skill_questions": [],
        "user_answer": "",
    }

    config = {"configurable": {"thread_id": thread_id}}
    state = interviewer.invoke(initial_state, config)
    print(f"Agent: {state['interview_log'][-1][1]}")

    # Conversation loop
    while state["stage"] != END:
        user_input = input("You: ")
        state["interview_log"].append(("User", user_input))
        state = interviewer.invoke(state, config)

        if state["interview_log"] and state["interview_log"][-1][0] == "Agent":
            print(f"Agent: {state['interview_log'][-1][1]}")

    print("\n--- Interview Finished ---")


if __name__ == "__main__":
    candidate_profile = UserProfile(id=uuid.uuid4())
    run_interview(candidate_profile)
