from google.adk.agents import SequentialAgent
from .sub_agents.research_agent import research_agent
from .sub_agents.analysis_agent import analysis_agent
from .sub_agents.summary_agent import summary_agent



root_agent = root_agent = SequentialAgent(
    name="research_pal",
    sub_agents=[research_agent, analysis_agent, summary_agent]
)