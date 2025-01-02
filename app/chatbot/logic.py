import logging
from typing import Dict, Any, Union, Tuple, Optional
from fastapi import HTTPException, status
from app.chatbot.core.graph import ChatBotGraph
from app.schemas.chatbot import UserMessage
from app.core.app_helper import get_app

logger = logging.getLogger(__name__)

class ChatbotError(Exception):
    """Base exception for chatbot-related errors"""
    def __init__(self, message: str, error_code: str = None):
        self.message = message
        self.error_code = error_code
        super().__init__(message)

def format_chat_input(message: str) -> Dict[str, Any]:
    """Format the user message into the expected graph input structure"""
    return {
        "messages": [("user", message)]
    }

def format_config(thread_id: Union[str, int]) -> Dict[str, Any]:
    """Format the configuration dictionary for graph processing"""
    return {
        "configurable": {
            "thread_id": str(thread_id)
        }
    }

async def get_graph() -> ChatBotGraph:
    """Retrieve and validate the graph from application state"""
    app = get_app()
    logger.info("Accessing app state graph")
    
    graph = getattr(app.state, "graph", None)
    if not graph:
        raise ChatbotError(
            "Chatbot service not initialized", 
            "GRAPH_NOT_INITIALIZED"
        )
    
    return graph

def extract_response_content(result: Dict[str, Any]) -> str:
    """Extract the response content from the graph result"""
    try:
        return result['messages'][-1].content
    except (KeyError, IndexError) as e:
        raise ChatbotError(
            "Invalid response structure from chatbot",
            "INVALID_RESPONSE"
        )

async def check_next_steps(graph: ChatBotGraph, config: Dict[str, Any]) -> Optional[str]:
    """Check if there are pending next steps in the graph state"""
    try:
        snapshot = await graph.aget_state(config)
        logger.info(f"State snapshot: {snapshot}")
        
        if hasattr(snapshot, 'next') and snapshot.next:
            logger.info(f"Next step required: {snapshot.next}")
            return "Need user approval for next step."
        return None
        
    except Exception as e:
        logger.error(f"Error checking graph state: {e}")
        raise ChatbotError(
            "Failed to check graph state",
            "STATE_CHECK_FAILED"
        )

def handle_error(e: Exception) -> str:
    """Convert various exceptions into appropriate error messages"""
    error_messages = {
        KeyError: "Invalid response structure.",
        ConnectionError: "Graph connection error.",
        AttributeError: "Unexpected response format from graph.",
        ChatbotError: lambda err: err.message
    }
    
    error_type = type(e)
    if error_type in error_messages:
        message = error_messages[error_type]
        if callable(message):
            return message(e)
        return message
    
    logger.error(f"Unexpected error: {e}", exc_info=True)
    return "An unexpected error occurred."

async def process_chat(user_message: UserMessage) -> str:
    """
    Process a user message through the chatbot's graph and return the assistant's response.

    Args:
        user_message (UserMessage): The user's input message.

    Returns:
        str: The chatbot's response message or an error message.
    """
    try:
        # Initialize and validate graph
        graph = await get_graph()
        
        # Prepare input data and config
        input_data = format_chat_input(user_message.msg)
        config = format_config(user_message.threadId)
        
        logger.debug(f"Processing message with Thread ID: {user_message.threadId}")
        
        # Process message through graph
        if(user_message.status == "approval"):
            result = await graph.ainvoke(None, config)
            logger.debug(f"Raw graph response: {result}")
        elif (user_message.status == "feedback"):
            snapshot = await graph.aget_state(config)
            logger.info(f"State snapshot: {snapshot}")

            last_message = snapshot.values["messages"][-1]
            tool_call = last_message.tool_calls[-1]
            msg = 'User requested changes: ' + user_message.msg
            input_data = format_chat_input(msg)
            tool_message = {
                "role": "tool",
                "content": input_data,
                "name": tool_call["name"],
                "tool_call_id": tool_call["id"],
            }
            new_messages = [tool_message]
            await graph.aupdate_state(
                config,
                {"messages": new_messages},
            )

            result = await graph.ainvoke(None, config)
            logger.debug(f"Raw graph response: {result}")
        else:
            result = await graph.ainvoke(input_data, config)
            logger.debug(f"Raw graph response: {result}")

        # result = await graph.ainvoke(input_data, config)
        # logger.debug(f"Raw graph response: {result}")
        
        # Check for next steps
        next_step = await check_next_steps(graph, config)
        if next_step:
            return next_step
        
        # Extract and return response
        logger.info(f"Returning chatbot response: {result}")
        return extract_response_content(result)
        
    except Exception as e:
        return handle_error(e)