from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini

from common.google_adk_setup import retry_config


PM_agent = Agent(
    name="portfolio_manager_agent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    instruction="""You are the best stock portfolio manager.
    Your task is to collate all the information from previous analyses.
    Output must include:
    1. percentage allocation of capital for each of the validated tickers.
    2. short term and long term plans for each of the validated tickers.
    """,
    output_key="portfolio_allocation",  # The result of this agent will be stored in the session state with this key.
)
