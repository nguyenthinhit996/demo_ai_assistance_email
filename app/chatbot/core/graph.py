from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph, START
from app.chatbot.core.state import ChatBotState
from app.chatbot.core.nodes.nodechatbot import node_call_llm
from langgraph.prebuilt import ToolNode, tools_condition
from app.chatbot.core.nodes.nodetools import node_run_tool
from app.chatbot.core.nodes.nodehummanreview import human_review_node
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langchain_core.messages import (
    AnyMessage,
)
from typing import (
    Any,
    Literal,
    Union,
)
from pydantic import BaseModel


def tools_condition(
    state: Union[list[AnyMessage], dict[str, Any], BaseModel],
    messages_key: str = "messages",
) -> Literal["human_review", "__end__"]:
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
    return "__end__"

class ChatBotGraph:
    graph: CompiledStateGraph

    def __init__(self, checkpointer):
       self.graph = self.graph_builder(checkpointer)

    def graph_builder(self, checkpointer: AsyncPostgresSaver):
        tool_node = ToolNode(tools=node_run_tool)
        graph = StateGraph(ChatBotState)

        graph.add_node("call_llm", node_call_llm)
        graph.add_node("run_tool", tool_node)
        graph.add_node("human_review", human_review_node)

        graph.add_edge(START, "call_llm")
        graph.add_edge("run_tool", "call_llm")
        graph.add_conditional_edges(
            "call_llm",
            tools_condition,
        )

        graph_complier = graph.compile(checkpointer=checkpointer)
        return graph_complier