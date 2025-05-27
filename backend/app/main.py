from fastapi import FastAPI, Request
from pydantic import BaseModel
from google.genai.types import Content, Part
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from app.agents.orchestrator import create_study_plan
import os
import logging

# --- Setup ---
app = FastAPI()
# Configure logging
#fast api allow CORS
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for dev; not safe for prod)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logger = logging.getLogger("uvicorn")
session_service = InMemorySessionService()
APP_NAME = "my_study_planner"

# --- Models ---
class ChatRequest(BaseModel):
    text: str
    session_id: str | None = None
    user_id: str | None = None

# --- Startup Event ---
@app.on_event("startup")
async def setup_adk():
    """Configure the ADK environment."""
    os.environ["GOOGLE_API_KEY"] = "your_api_key_here"
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "FALSE"
    logger.info("ADK environment configured.")

# --- API Endpoints ---
@app.get("/new-session")
async def new_session(user_id: str = "student_9yo"):
    session = await session_service.create_session(app_name=APP_NAME, user_id=user_id, state={})
    logger.info(f"New session created: {session.id}")
    return session

@app.get("/list-sessions")
async def list_sessions(user_id: str = "student_9yo"):
    sessions = await session_service.list_sessions(app_name=APP_NAME, user_id=user_id)
    return {"sessions": sessions}

@app.post("/chat")
async def chat(request: ChatRequest):
    response = await create_study_plan(session_service, request)
    return response
