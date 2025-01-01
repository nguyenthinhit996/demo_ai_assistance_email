
from app.chatbot.core.state import ChatBotState
from langchain_openai import ChatOpenAI
from app.chatbot.core.nodes.nodetools import tools
from app.core import config

#  # Create a settings instance
# settings = config.Settings()

# # Print the loaded values for debugging
# print(f"OpenAI API Key: {settings.openai_api_key}")
# print(f"LangChain API Key: {settings.langchain_api_key}")
# print(f"LangChain Tracing: {settings.langchain_tracing_v2}")
# print(f"LangChain Endpoint: {settings.langchain_endpoint}")
# print(f"LangChain Project: {settings.langchain_project}")
# print(f"Tavily API Key: {settings.tavily_api_key}")

llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(tools)

def nodechatbot(state: ChatBotState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}