from fastapi import FastAPI
from pydantic import BaseModel


class Request(BaseModel):
    company_id: str
    user_id: str


class ListMessagesController:
    def __init__(self, app: FastAPI):
        @app.get("/messages")
        async def _(request: Request):
            return self.handle(request)

    def handle(self, request: Request):
        return []
