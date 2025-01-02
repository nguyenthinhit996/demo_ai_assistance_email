
from app.chatbot.core.state import ChatBotState
from langchain_openai import ChatOpenAI
from app.chatbot.core.nodes.nodetools import tools
from app.core import config

#  # Create a settings instance
settings = config.Settings()

llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(tools)

def nodechatbot(state: ChatBotState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}