from fastapi import APIRouter, HTTPException
from app.chatbot.logic import process_chat
from app.schemas.chatbot import UserMessage
from fastapi import FastAPI, Request
from IPython.display import Image, display
from app.core.app_helper import get_app
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/")
async def chat(user_message: UserMessage):
    try:
        response = await process_chat(user_message)
        return {"user_message": user_message, "bot_response": response}
    except Exception as e:
        print("Error processing", {e})
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generateimage")
async def chat():
    try:
        app = get_app()

        graph = getattr(app.state, "graph", None)
        logger.info(f"Accessing app state graph {graph}")
        display(Image(graph.get_graph().draw_mermaid_png()))
    except Exception as e:
        logger.error(f"Error generating image: {e}")
        # This requires some extra dependencies and is optional
        pass