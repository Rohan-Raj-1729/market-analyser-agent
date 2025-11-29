from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini

from common.google_adk_setup import retry_config
from universe_definition_agent.tools import validate_universe


UDA_agent = LlmAgent(
    name="universe_definition_agent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""
    You are the Universe Definition & Validation Agent.
    Your goal is to clean, validate, and refine the list of stocks before deeper research.
    For any request involving stock filtering, validation, or eligibility checks:

    Always begin by using validate_universe() by passing list of tickers.
    Stocks failing any test must be excluded with a clear reason.
    If any tool returns "error", report the issue clearly and suggest what input may need correction.
    Your output must include:
    1. A "Validated Stocks" list with brief justification for each approved ticker.
    2. An "Excluded Stocks" list with specific failure reasons for each tool.
    3. For "Validated Stocks", store ticker and market cap
    No speculation: strictly use tool-derived data.

    Your purpose is to deliver a clean, defensible universe for downstream agents.
    No assumptions, no guesses — only tool-verified facts.

    """,
    tools=[validate_universe],
    output_key="universe_definition",
)
