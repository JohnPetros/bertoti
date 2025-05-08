from fastapi import FastAPI
from pydantic import BaseModel

from src.database import chat_message_repository


class Request(BaseModel):
    company_id: str
    user_id: str


class ListMessagesController:
    def __init__(self, app: FastAPI):
        @app.get("/messages")
        async def _(request: Request):
            return chat_message_repository.find_many_by_user_and_company(
                request.user_id, request.company_id
            )
