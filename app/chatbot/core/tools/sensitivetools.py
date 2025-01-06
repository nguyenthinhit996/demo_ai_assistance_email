 
from typing import List
from langchain_core.tools import BaseTool
from app.chatbot.core.tools.request.updaterequest import UpdateRequestTool



class SensitveTools:
    tools: List[BaseTool]
    
    def __init__(self, tools=None):
        if tools is None:
            tools = []
        self.tools = tools

sensitvetool_tools = SensitveTools([UpdateRequestTool()]).tools

sensitive_tool_names = {t.name for t in sensitvetool_tools}