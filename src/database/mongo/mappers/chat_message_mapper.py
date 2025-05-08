from src.core.structures import ChatMessage


class ChatMessageMapper:
    @staticmethod
    def to_entity(model: dict):
        return ChatMessage(
            user_id=model["userId"],
            company_id=model["companyId"],
            content=model["content"],
            sender=model["sender"],
            sent_at=model["sentAt"],
        )

    @staticmethod
    def to_model(entity: ChatMessage):
        return {
            "userId": entity.user_id,
            "companyId": entity.company_id,
            "content": entity.content,
            "sender": entity.sender,
            "sentAt": entity.sent_at,
        }
