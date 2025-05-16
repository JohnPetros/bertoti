from fastapi import APIRouter
from pydantic import BaseModel
from src.chatbot import AdkChatbotAgent

from src.core.structures.chat_message import ChatMessage


class Request(BaseModel):
    company_id: str
    user_role: str
    message: str


class SendMessageController:
    def __init__(self, router: APIRouter):
        @router.post("/messages/{user_id}/{session_id}")
        async def _(user_id: str, session_id: str, request: Request) -> ChatMessage:
            agent = AdkChatbotAgent()
            answer = await agent.answer_message(
                message=request.message,
                company_id=request.company_id,
                user_id=user_id,
                session_id=session_id,
                user_role=request.user_role,
            )
            return ChatMessage(
                content=answer,
                sender="bot",
            )
