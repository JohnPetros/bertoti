from fastapi import FastAPI
from .controllers.list_messages_controller import ListMessagesController
from .controllers.send_message_controller import SendMessageController

app = FastAPI()

ListMessagesController(app)
SendMessageController(app)
