from fastapi import APIRouter, HTTPException
from app.chatbot.logic import process_chat
from app.schemas.chatbot import UserMessage
from fastapi import FastAPI, Request

router = APIRouter()

@router.post("/")
async def chat(user_message: UserMessage):
    try:
        response = await process_chat(user_message)
        return {"user_message": user_message, "bot_response": response}
    except Exception as e:
        print("Error processing", {e})
        raise HTTPException(status_code=500, detail=str(e))
