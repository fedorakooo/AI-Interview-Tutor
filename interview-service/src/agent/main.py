import uuid

from langgraph.constants import END

from src.agent.data.sample_data import SAMPLE_CV
from src.agent.domain.models.interview_state import InterviewState
from src.agent.domain.models.user_profile import UserProfile
from src.agent.domain.value_objects.interview_stage import InterviewStage
from src.agent.state.soft_questions import choose_soft_questions
from src.agent.workflow import create_interview_workflow


def run_interview(profile: UserProfile):
    interviewer = create_interview_workflow()
    thread_id = str(uuid.uuid4())

    initial_state: InterviewState = {
        "developer_profile": profile,
        "interview_log": [],
        "stage": InterviewStage.GREETING,
        "cv_data": SAMPLE_CV,
        "soft_questions_turns": 0,
        "soft_questions": choose_soft_questions(),
    }

    config = {"configurable": {"thread_id": thread_id}}
    state = interviewer.invoke(initial_state, config)

    if state["interview_log"]:
        print(f"{state['interview_log'][-1][0]} {state['interview_log'][-1][1]}")

    while state["stage"] != END:

        user_input = input("You: ")
        state["interview_log"].append(("User", user_input))

        state = interviewer.invoke(state, config)

        if state["interview_log"] and state["interview_log"][-1][0] == "Agent":
            print(f"Agent: {state['interview_log'][-1][1]}")


if __name__ == "__main__":
    candidate_profile = UserProfile(id=uuid.uuid4())
    run_interview(candidate_profile)
