import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import LlmAgent
from app.prompts.prompts import (
    STUDY_CONTENT_AGENT_INSTRUCTION,
)
from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from app.models.models import DayPlan
from app.callbacks.before_callback import rate_limit_callback
from app.callbacks.guardrails import check_if_agent_should_run

study_content_agent = LlmAgent(
    name="study_content_agent",
    model="gemini-2.0-flash",
    description=(
        "Agent to help with generation of study content for each topic" ),
    instruction=(STUDY_CONTENT_AGENT_INSTRUCTION),
    output_schema=DayPlan,  # Enforce JSON output
    output_key="study_plan_content",  # Key to use in the output JSON
    before_model_callback=rate_limit_callback, # Apply rate limiting callback
    before_agent_callback=check_if_agent_should_run  # Apply rate limiting callback
)