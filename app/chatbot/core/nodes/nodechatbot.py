
from app.chatbot.core.state import ChatBotState
from langchain_openai import ChatOpenAI
from app.chatbot.core.nodes.nodetools import node_run_tool
from app.core import config
from langgraph.utils.config import get_configurable
import logging
logger = logging.getLogger(__name__)


#  # Create a settings instance
settings = config.Settings()

llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(node_run_tool)

def node_call_llm(state: ChatBotState):
    logger.debug(f"Calling LLM with state: {get_configurable()}")
    return {"messages": [llm_with_tools.invoke(state["messages"])]}