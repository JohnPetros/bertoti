from dotenv import load_dotenv

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from src.controllers import ListMessagesController, SendMessageController

load_dotenv()

app = FastAPI()
router = APIRouter(prefix="/chatbot")

ListMessagesController(router)
SendMessageController(router)

app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
