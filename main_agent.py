from google.adk.agents import SequentialAgent, ParallelAgent
from google.adk.runners import Runner

from common.google_adk_setup import session_service, memory_service
from fundamentals_analyst_agent.agent import FAA_agent
from market_sentiment_analyst_agent.agent import MSA_agent
from technical_analyst_agent.agent import TA_agent
from universe_definition_agent.agent import UDA_agent
from portfolio_manager_agent.agent import PM_agent


parallel_agent = ParallelAgent(
    name="market_analyst",
    sub_agents=[FAA_agent, MSA_agent, TA_agent]
)
root_agent = SequentialAgent(
    name="portofolio_manager_agent",
    sub_agents=[UDA_agent, parallel_agent, PM_agent]
)

agent_runner = Runner(agent=root_agent, app_name="Portfolio Manager", session_service=session_service, memory_service=memory_service)