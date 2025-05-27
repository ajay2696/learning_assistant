import time
import logging
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmRequest
from typing import Any, Dict, Optional, Tuple
from google.adk.tools import BaseTool
from google.adk.agents.invocation_context import InvocationContext
from google.adk.sessions.state import State
from google.adk.tools.tool_context import ToolContext

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Rate limiting configuration
RATE_LIMIT_WINDOW_SECS = 60
MAX_REQUESTS_PER_WINDOW = 10


def rate_limit_callback(
    callback_context: CallbackContext, 
    llm_request: LlmRequest
) -> None:
    """
    Implements a sliding window rate limit for LLM requests.
    
    Enforces a maximum number of requests per time window to prevent API quota exhaustion.
    If the rate limit is exceeded, the function will sleep until the window resets.
    
    Args:
        callback_context: CallbackContext object representing the active callback context
        llm_request: LlmRequest object representing the active LLM request
    """
    
    # Sanitize empty text parts to prevent API issues
    for content in llm_request.contents:
        for part in content.parts:
            if part.text == "":
                part.text = " "
    
    current_time = time.time()
    
    # Initialize rate limiting state if not present
    if "timer_start" not in callback_context.state:
        callback_context.state["timer_start"] = current_time
        callback_context.state["request_count"] = 1
        logger.debug(
            "Rate limit initialized - timestamp: %.0f, request_count: 1, elapsed_secs: 0",
            current_time
        )
        return
    
    # Calculate current window metrics
    timer_start = callback_context.state["timer_start"]
    current_count = callback_context.state["request_count"]
    elapsed_time = current_time - timer_start
    new_count = current_count + 1
    
    logger.debug(
        "Rate limit check - timestamp: %.0f, request_count: %d, elapsed_secs: %.1f",
        current_time, new_count, elapsed_time
    )
    
    # Check if we've exceeded the rate limit within the current window
    if new_count > MAX_REQUESTS_PER_WINDOW:
        # Calculate remaining time in current window
        remaining_window_time = RATE_LIMIT_WINDOW_SECS - elapsed_time
        sleep_duration = remaining_window_time + 1  # Add 1 second buffer
        
        if sleep_duration > 0:
            logger.warning(
                "Rate limit exceeded (%d/%d requests). Sleeping for %.1f seconds",
                new_count, MAX_REQUESTS_PER_WINDOW, sleep_duration
            )
            time.sleep(sleep_duration)
        
        # Reset the rate limiting window
        callback_context.state["timer_start"] = time.time()  # Use current time after sleep
        callback_context.state["request_count"] = 1
        
        logger.debug("Rate limit window reset")
    else:
        # Update request count within current window
        callback_context.state["request_count"] = new_count