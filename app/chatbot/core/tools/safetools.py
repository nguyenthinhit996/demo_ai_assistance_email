 
from typing import Annotated, List
from langchain_core.tools import BaseTool
from app.core import config




class SafeTools:
    tools: List[BaseTool]
    
    def __init__(self, tools=None):
        if tools is None:
            tools = []
        self.tools = tools
