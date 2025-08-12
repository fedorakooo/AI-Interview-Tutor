import json
import logging
import random

from langchain_core.prompts import ChatPromptTemplate
from langgraph.constants import END

from src.agent.config import SOFT_QUESTIONS_JSON_PATH
from src.agent.domain.models.cv_data import CVData
from src.agent.domain.models.interview_state import InterviewState
from src.agent.domain.value_objects.conversation_role import ConversationRole
from src.agent.domain.value_objects.interview_stage import InterviewStage
from src.agent.llm import llm


def choose_soft_questions() -> list[str]:
    with open(SOFT_QUESTIONS_JSON_PATH) as json_file:
        data = json.load(json_file)

    number_of_questions = random.choice([2, 3])
    selected_questions = random.sample(data, number_of_questions)

    logging.info(f"Selected {number_of_questions} soft questions: {selected_questions}")
    return selected_questions


def rephrase_question(question: str, context: str, cv: CVData) -> str:
    logging.debug("Rephrasing question: %s", question)
    prompt_template = ChatPromptTemplate.from_template(
        """
You are an interview assistant.
Based on the following interview conversation context and candidate's CV,
rephrase the original question below to make it concise, natural, and fitting the tone of the conversation so far.

IMPORTANT: Return ONLY the rephrased question. Do not add any explanations, comments, or additional text.

Interview context:
{context}

Candidate CV:
{cv}

Original question:
{question}

Rephrased question:"""
    )
    chain = prompt_template | llm
    response = chain.invoke(
        {
            "cv": str(cv),
            "context": context,
            "question": question,
        }
    ).content.strip()

    logging.info(f"Rephrased question: {response}")
    return response


def ask_soft_questions(state: InterviewState) -> InterviewState:
    logging.debug("Entering ask_soft_questions with state: {state}", state)

    interview_log = state.get("interview_log", [])
    soft_questions = state.get("soft_questions", [])
    cv_data = state.get("cv_data", {})
    soft_questions_turns = state.get("soft_questions_turns", 0)

    state["stage"] = InterviewStage.SOFT_QUESTIONS

    if not soft_questions or soft_questions_turns >= 6:
        logging.info("No more soft questions or maximum turns reached. Ending soft questions stage.")
        state["stage"] = END
        return state

    state["soft_questions_turns"] = soft_questions_turns + 1
    original_question = soft_questions[-1]

    conversation_context = "\n".join([entry[1] for entry in interview_log])

    logging.debug("Deciding between small talk and asking question.")
    decision_prompt = ChatPromptTemplate.from_template(
        """
You are an exceptionally polite and tactful interview assistant.
Your role is to maintain a warm, professional, and respectful tone at all times.

Based on the interview context and candidate's CV,
decide whether to:
- continue with a short, friendly small talk phrase that smoothly fits the flow, OR
- politely ask the next prepared soft question.

You MUST return ONLY one of the following words (without quotes or punctuation):
SMALLTALK
QUESTION

Interview context:
{conversation_context}

Candidate CV:
{cv_summary}

Next soft question:
{original_question}

Your choice:"""
    )
    chain = decision_prompt | llm
    decision = (
        chain.invoke(
            {
                "conversation_context": conversation_context,
                "cv_summary": json.dumps(cv_data, indent=2),
                "original_question": original_question,
            }
        )
        .content.strip()
        .upper()
    )

    logging.info("Decision made by LLM: %s", decision)

    if decision == "SMALLTALK":
        logging.debug("Generating small talk phrase.")
        prompt_template = ChatPromptTemplate.from_template(
            """
You are an exceptionally polite and tactful interview assistant.
Instead of asking a new question, say one short, friendly phrase to keep the conversation flowing naturally.
Be warm, respectful, and professional.

Interview context:
{conversation_context}

Candidate CV:
{cv_summary}

Small talk phrase:"""
        )
        chain = prompt_template | llm
        response = chain.invoke(
            {
                "conversation_context": conversation_context,
                "cv_summary": json.dumps(cv_data, indent=2),
            }
        ).content.strip()

        logging.info("Small talk generated: %s", response)
        interview_log.append((ConversationRole.AGENT, response))

    else:  # QUESTION
        logging.debug("Rephrasing the next soft question.")
        prompt_template = ChatPromptTemplate.from_template(
            """
You are an exceptionally polite and tactful interview assistant.
Based on the conversation so far and the candidate's CV,
rephrase the original question so it sounds concise, natural, and warmly respectful.

IMPORTANT: Return ONLY the rephrased question — no explanations or extra text.

Interview context:
{conversation_context}

Candidate CV:
{cv_summary}

Original question:
{original_question}

Rephrased question:"""
        )
        chain = prompt_template | llm
        rephrased_question = chain.invoke(
            {
                "conversation_context": conversation_context,
                "cv_summary": json.dumps(cv_data, indent=2),
                "original_question": original_question,
            }
        ).content.strip()

        logging.info("Rephrased question: %s", rephrased_question)
        interview_log.append((ConversationRole.AGENT, rephrased_question))

    state["soft_questions"] = soft_questions
    state["interview_log"] = interview_log
    logging.debug("Updated state after asking soft question: %s", state)
    return state
