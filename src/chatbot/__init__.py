from .runner import Runner


class AdkChatbotAgent:
    def __init__(self):
        self.runner = Runner()

    async def answer_message(
        self,
        message: str,
        company_id: str,
        user_id: str,
        session_id: str,
        user_role: str,
    ):
        return await self.runner.answer_message(
            query=message,
            company_id=company_id,
            user_id=user_id,
            session_id=session_id,
            user_role=user_role,
        )

    def get_all_messages(self, user_id: str, session_id: str):
        return self.runner.get_all_messages(user_id, session_id)
