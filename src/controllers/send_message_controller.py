from fastapi import FastAPI
from pydantic import BaseModel
from src.chatbot import AdkChatbotAgent


class Request(BaseModel):
    company_id: str
    user_id: str
    message: str


class SendMessageController:
    def __init__(self, app: FastAPI):
        @app.post("/message")
        async def _(request: Request):
            agent = AdkChatbotAgent()
            answer = await agent.start(
                query=request.message,
                user_id=request.user_id,
                company_id=request.company_id,
            )
            return answer
