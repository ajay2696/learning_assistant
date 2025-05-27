import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import LlmAgent
from app.tools.tools import get_curriculum
from app.agents.sub_agents.study_planner.study_planner_agent import study_planner_agent
from app.agents.sub_agents.study_content.study_content_agent import study_content_agent
from app.agents.sub_agents.quiz.quiz_preparation_agent import quiz_preparation_agent

root_agent = LlmAgent(
    name="root_agent",
    model="gemini-2.0-flash",
    description=(
        "Use other agents to generate the study plan, quizzes and study content for students. "
    ),
    instruction=("Your are a root agent with other subagents to help generation of study plans, quizzes and study content forstudents. ")
)