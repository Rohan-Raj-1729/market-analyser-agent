from google.genai import types
from google.adk.memory import InMemoryMemoryService
from google.adk.sessions import InMemorySessionService


retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
)

session_service = InMemorySessionService()
memory_service = (
    InMemoryMemoryService()
)  # ADK's built-in Memory Service for development and testing
