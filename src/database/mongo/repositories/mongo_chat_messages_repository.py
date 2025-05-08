from src.core.structures import ChatMessage
from src.database.mongo.mappers import ChatMessageMapper

from src.database.mongo.mongo import mongo


class MongoChatMessageRepository:
    def __init__(self, db_name: str = "chatbot"):
        self.collection = mongo[db_name]["chatMessages"]

    def find_many_by_user_and_company(self, user_id: str, company_id: str):
        models = self.collection.find({"userId": user_id, "companyId": company_id})
        return [ChatMessageMapper.to_entity(model) for model in models]

    def add(self, chat_message: ChatMessage):
        return self.collection.insert_one(ChatMessageMapper.to_model(chat_message))
