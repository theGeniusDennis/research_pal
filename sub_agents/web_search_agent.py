from google.adk.agents import Agent
from google.adk.tools import google_search


prompt = """
    You are a web search specialist. Your only job is to search the web for information on the given topic.
- Run thorough searches to gather as much relevant information as possible
- Return raw, detailed results — do not summarize or filter
- Always include the source URLs with each piece of information
- Search multiple angles of the topic if needed
- Do not add opinions or conclusions — just return what you find

"""


web_search_agent = Agent(
    name="web_search_agent",
    model="gemini-2.5-flash",
    description="Searches the web for general information, facts, research papers, and broad topic coverage on any given subject.",
    instruction=prompt,
    tools=[google_search]
)