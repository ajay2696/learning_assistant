from typing import Optional
from google.genai import types # For types.Content
from google.adk.agents.callback_context import CallbackContext
from typing import Optional

# Define a basic list of safety words (this can be replaced with a more sophisticated filter later)
SAFETY_WORDS = {"harm", "violence", "hate", "attack", "kill", "explosive", "suicide", "threat"}

def contains_safety_words(text: str) -> bool:
    """Simple check for safety words in the input text."""
    lowered = text.lower()
    return any(word in lowered for word in SAFETY_WORDS)

# --- 1. Define the Callback Function ---
def check_if_agent_should_run(callback_context:CallbackContext) -> Optional[types.Content]:
    """
    Guardrail: Check if input contains safety words.
    If so, skip agent execution and return a safety warning message.
    """
    agent_name = callback_context.agent_name
    invocation_id = callback_context.invocation_id
    current_state = callback_context.state.to_dict()

    print(f"\n[Callback] Entering agent: {agent_name} (Inv: {invocation_id})")
    print(f"[Callback] Current State: {current_state}")

    if contains_safety_words(str(current_state)):
        print(f"[Callback] Safety violation detected: Skipping agent {agent_name}.")
        return types.Content(
            parts=[types.Part(text=f"⚠️ Agent {agent_name} skipped due to unsafe content in input.")],
            role="model"
        )

    if current_state.get("skip_llm_agent", False):
        print(f"[Callback] State condition 'skip_llm_agent=True' met: Skipping agent {agent_name}.")
        return types.Content(
            parts=[types.Part(text=f"Agent {agent_name} skipped due to state condition.")],
            role="model"
        )

    print(f"[Callback] No issues: Proceeding with agent {agent_name}.")
    return None
