from fastapi import FastAPI
from pydantic import BaseModel
from ..ai import ChatbotSquad


class Request(BaseModel):
    company_id: str
    user_id: str
    message: str


class SendMessageController:
    def __init__(self, app: FastAPI):
        @app.post("/message")
        async def _(request: Request):
            return self.handle(request)

    def handle(self, request: Request):
        squad = ChatbotSquad()
        answer = squad.start(
            question=request.message,
            company_id=request.company_id,
            user_id=request.user_id,
        )
        return answer
