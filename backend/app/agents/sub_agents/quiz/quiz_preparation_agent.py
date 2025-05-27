import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import LlmAgent
from app.prompts.prompts import (QUIZ_GENERATION_AGENT_INSTRUCTION)
from app.models.models import QuizDay
from app.callbacks.before_callback import rate_limit_callback

quiz_preparation_agent = LlmAgent(
    name="quiz_preparation_agent",
    model="gemini-2.0-flash",
    description=(
        "Agent will prepare questions and quizzes for a topic to display in user interface"
    ),
    instruction=(QUIZ_GENERATION_AGENT_INSTRUCTION),
    output_schema=QuizDay,  # Enforce JSON output
    output_key="study_plan_quiz_content", # Key to use in the output JSON
    before_model_callback=rate_limit_callback  # Apply rate limiting callback
)