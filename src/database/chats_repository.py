from pymongo import MongoClient

mongo = MongoClient("mongodb://localhost:27017")


class ChatsRepository:
    def __init__(self, db_name: str = "chatgpt"):
        self.db = mongo[db_name]
        self.collection = self.db["chats"]

    def get_all_chats(self):
        return list(self.collection.find())

    def get_chat_by_id(self, chat_id: str):
        return self.collection.find_one({"_id": chat_id})

    def add_chat(self, chat_data: dict):
        return self.collection.insert_one(chat_data)

    def update_chat(self, chat_id: str, chat_data: dict):
        return self.collection.update_one({"_id": chat_id}, {"$set": chat_data})

    def delete_chat(self, chat_id: str):
        return self.collection.delete_one({"_id": chat_id})
