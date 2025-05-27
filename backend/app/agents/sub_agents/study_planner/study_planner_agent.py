import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import LlmAgent
from app.prompts.prompts import (
    STUDY_PLANNER_AGENT_INSTRUCTION
)
from pydantic import BaseModel, Field
from typing import List
from app.models.models import QuizDay, DayPlan, StudyPlanOutput
from app.callbacks.before_callback import rate_limit_callback
from app.callbacks.guardrails import check_if_agent_should_run

study_planner_agent = LlmAgent(
    name="root_agent",
    model="gemini-2.0-flash",
    description=("Agent to help with creating study plans for students based on the grade and topic name"),
    instruction=( STUDY_PLANNER_AGENT_INSTRUCTION  ),
    output_schema = StudyPlanOutput, # Enforce JSON output
    output_key="study_plan",  # Key to use in the output JSON
    before_model_callback=rate_limit_callback,  # Apply rate limiting callback
    before_agent_callback=check_if_agent_should_run  # Apply rate limiting callback
)