from langchain_community.tools.tavily_search import TavilySearchResults
from typing import Annotated, List
from langchain_core.tools import BaseTool


class ChatBotTools:
    tools: List[BaseTool]
    def __init__(self):
        self.tools = [
            self.seach_tavily_tool()
        ]
    def seach_tavily_tool(self):
        tool = TavilySearchResults(max_results=2)
        return tool

tools = ChatBotTools().tools
