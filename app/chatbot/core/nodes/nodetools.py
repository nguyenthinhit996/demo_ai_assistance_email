from langchain_community.tools.tavily_search import TavilySearchResults
from typing import Annotated, List
from langchain_core.tools import BaseTool
from app.core import config
from app.chatbot.core.tools.submistiontools import GetRequestTool

from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

 # Create a settings instance
settings = config.Settings()

class ChatBotTools:
    tools: List[BaseTool]
    def __init__(self):
        self.tools = [
            self.seach_tavily_tool(),
            GetRequestTool()
        ]
    def seach_tavily_tool(self):
        tool = TavilySearchResults(max_results=2)
        return tool

node_run_tool = ChatBotTools().tools
