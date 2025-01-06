 
from typing import List
from langchain_core.tools import BaseTool
from app.chatbot.core.tools.request.getrequest import GetRequestTool



class SafeTools:
    tools: List[BaseTool]
    
    def __init__(self, tools=None):
        if tools is None:
            tools = []
        self.tools = tools

safe_tools = SafeTools([GetRequestTool()]).tools