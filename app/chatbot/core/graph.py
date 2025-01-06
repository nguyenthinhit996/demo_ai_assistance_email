from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph, START, END
from langchain_core.runnables import RunnableLambda
from app.chatbot.core.state import ChatBotState
from app.chatbot.core.nodes.nodechatbot import Assistant
from langgraph.prebuilt import ToolNode
from app.chatbot.core.nodes.nodetools import node_run_tool
from app.chatbot.core.nodes.nodehummanreview import human_review_node
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langchain_core.messages import (
    AnyMessage,
)
import logging
from typing import (
    Any,
    Literal,
    Union,
)
from pydantic import BaseModel
from app.chatbot.core.tools.safetools import safe_tools
from app.chatbot.core.tools.sensitivetools import sensitvetool_tools, sensitive_tool_names
from app.chatbot.core.tools.util.summarizeconversation import summarize_conversation_tool
from app.core import config


settings = config.Settings()
logger = logging.getLogger(__name__)

def tools_condition(
    state: Union[list[AnyMessage], dict[str, Any], BaseModel],
    messages_key: str = "messages",
) -> Literal["human_review", None]:
    if isinstance(state, list): 
        ai_message = state[-1]
    elif isinstance(state, dict) and (messages := state.get(messages_key, [])):
        ai_message = messages[-1]
    elif messages := getattr(state, messages_key, []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "human_review"
    return None

def handle_tool_error(state) -> dict:
    error = state.get("error")
    tool_calls = state["messages"][-1].tool_calls
    logger.error(f"tool_calls {tool_calls}, error: {error}")

def route_condition(state: ChatBotState) -> Literal["human_review", "summarize_conversation", "__end__"]:
    messages = state["messages"]
    next_node = tools_condition(state)
    if next_node == "human_review":
        return "human_review"
    if len(messages) > settings.length_of_messages_to_summarize:
        return "summarize_conversation"
    return "__end__"

class ChatBotGraph:
    graph: CompiledStateGraph

    def __init__(self, checkpointer):
       self.graph = self.graph_builder(checkpointer)

    def graph_builder(self, checkpointer: AsyncPostgresSaver):
        
        tool_safe_node = ToolNode(tools=safe_tools).with_fallbacks(
            [RunnableLambda(handle_tool_error)], exception_key="error"
        )

        tool_sensitvetool_node = ToolNode(tools=sensitvetool_tools).with_fallbacks(
            [RunnableLambda(handle_tool_error)], exception_key="error"
        )

        graph = StateGraph(ChatBotState)

        graph.add_node("call_llm", Assistant())
        graph.add_node("run_safe_tools", tool_safe_node)
        graph.add_node("run_sensitive_tools", tool_sensitvetool_node)
        graph.add_node("human_review", human_review_node)
        graph.add_node("summarize_conversation", summarize_conversation_tool)

        graph.add_edge(START, "call_llm")
        graph.add_edge("run_safe_tools", "call_llm")
        graph.add_edge("run_sensitive_tools", "call_llm")
        graph.add_conditional_edges(
            "call_llm",
            route_condition,
        )

        graph_complier = graph.compile(checkpointer=checkpointer)
        return graph_complier