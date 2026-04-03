from google.adk.agents import ParallelAgent
from .web_search_agent import web_search_agent
from .news_agent import news_agent



research_agent = ParallelAgent(
    name="research_agent",
    sub_agents=[web_search_agent, news_agent]
)
