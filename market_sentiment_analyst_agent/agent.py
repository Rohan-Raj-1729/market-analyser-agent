from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search

from common.google_adk_setup import retry_config


MSA_agent = Agent(
    name="market_sentiment_analyst_agent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    instruction="""You are a news research agent specialized in market sentiment analysis of stocks.
    Given a list of stock tickers, collect latest news about the stocks and perform sentiment analysis for each of those.
    Output must include:
    1. A verdict on both short term and long term investment for each stock: ['STRONG BUY', 'STRONG SELL', 'HOLD', 'BUY', 'SELL']
    """,
    tools=[google_search],
    output_key="market_sentiment_analysis"
)
