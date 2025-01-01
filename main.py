from fastapi import FastAPI
from app.api.routes import auth, chatbot, crud, vector_search
from app.core.startup import create_app

from app.core.app_helper import set_app

import logging


logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


# Create the FastAPI app with the lifespan handler
app = create_app()

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(chatbot.router, prefix="/chatbot", tags=["Chatbot"])
app.include_router(crud.router, prefix="/crud", tags=["CRUD"])
app.include_router(vector_search.router, prefix="/vector", tags=["Vector Search"])

set_app(app)