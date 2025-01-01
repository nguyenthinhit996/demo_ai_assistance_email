import logging
from fastapi import FastAPI
from app.chatbot.core.graph import ChatBotGraph
from app.schemas.chatbot import UserMessage
from app.core.app_helper import get_app

logger = logging.getLogger(__name__)

async def process_chat(user_message: UserMessage) -> str:
    """
    Process a user message through the chatbot's graph and return the assistant's response.

    Args:
        user_message (UserMessage): The user's input message.

    Returns:
        str: The chatbot's response message or an error message.
    """
    app = get_app()
    logger.info("Accessing app state graph.")

    try:
        # Ensure the graph is initialized in the app state
        graph = getattr(app.state, "graph", None)
        if graph is None:
            raise RuntimeError("The graph is not initialized in the application state.")

        logger.debug(f"Processing message with Thread ID: {user_message.threadId}")

        # Prepare input data and configuration for the graph invocation
        input_data = {"messages": [("user", user_message.msg)]}
        config = {"configurable": {"thread_id": str(user_message.threadId)}}

        # Invoke the graph asynchronously
        result = await graph.ainvoke(input_data, config)

        # Log the raw result for debugging
        logger.info(f"Generated raw response: {result}")
        

    except KeyError as e:
        logger.error(f"Key error in graph result: {e}")
        return "Invalid response structure."
    except ConnectionError as e:
        logger.error(f"Connection issue with graph: {e}")
        return "Graph connection error."
    except AttributeError as e:
        logger.error(f"Attribute error accessing result: {e}")
        return "Unexpected response format from graph."
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return "An unexpected error occurred."
