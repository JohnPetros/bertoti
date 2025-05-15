from fastapi import FastAPI
from pydantic import BaseModel

from src.chatbot import AdkChatbotAgent


class Request(BaseModel):
    user_id: str
    session_id: str


class ListMessagesController:
    def __init__(self, app: FastAPI):
        @app.get("/messages")
        async def _(request: Request):
            agent = AdkChatbotAgent()
            return agent.get_all_messages(request.user_id, request.session_id)
