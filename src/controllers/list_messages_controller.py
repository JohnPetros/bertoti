from fastapi import APIRouter

from src.chatbot import AdkChatbotAgent


class ListMessagesController:
    def __init__(self, router: APIRouter):
        @router.get("/messages/{user_id}/{session_id}")
        async def _(user_id: str, session_id: str):
            agent = AdkChatbotAgent()
            return agent.get_all_messages(user_id, session_id)
