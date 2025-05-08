from fastapi import FastAPI

from src.controllers import ListMessagesController, SendMessageController

app = FastAPI()

ListMessagesController(app)
SendMessageController(app)
