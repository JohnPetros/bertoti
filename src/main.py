from dotenv import load_dotenv

from fastapi import FastAPI

from src.controllers import ListMessagesController, SendMessageController

load_dotenv()

app = FastAPI()

ListMessagesController(app)
SendMessageController(app)
