from .runner import Runner


class AdkChatbotAgent:
    def __init__(self):
        self.runner = Runner()

    async def start(self, question: str, user_id: str, company_id: str):
        return await self.runner.start(question, user_id, company_id)

    def get_all_messages(self, user_id: str):
        return self.runner.get_all_messages(user_id)
