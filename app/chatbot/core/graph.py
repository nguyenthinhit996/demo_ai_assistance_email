from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph, START, END
from app.chatbot.core.state import ChatBotState
from app.chatbot.core.nodes.nodechatbot import nodechatbot
from langgraph.prebuilt import ToolNode, tools_condition
from app.chatbot.core.nodes.nodetools import tools
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from app.core import config

 # Create a settings instance
settings = config.Settings()

# Print the loaded values for debugging
# print(f"OpenAI API Key: {settings.openai_api_key}")
# print(f"LangChain API Key: {settings.langchain_api_key}")
# print(f"LangChain Tracing: {settings.langchain_tracing_v2}")
# print(f"LangChain Endpoint: {settings.langchain_endpoint}")
# print(f"LangChain Project: {settings.langchain_project}")
# print(f"Tavily API Key: {settings.tavily_api_key}")

class ChatBotGraph:
    graph: CompiledStateGraph

    def __init__(self, checkpointer):
       self.graph = self.graph_builder(checkpointer)

    def graph_builder(self, checkpointer: AsyncPostgresSaver):
       
        graph = StateGraph(ChatBotState)
        graph.add_node("chatbot", nodechatbot)

        tool_node = ToolNode(tools=tools)
        graph.add_node("tools", tool_node)

        # Condition for when a tool is called or END
        graph.add_conditional_edges(
            "chatbot",
            tools_condition,
        )
        
        # Any time a tool is called, we return to the chatbot to decide the next step
        graph.add_edge("tools", "chatbot")
        graph.add_edge(START, "chatbot")
        graph_complier = graph.compile(checkpointer=checkpointer)
        return graph_complier