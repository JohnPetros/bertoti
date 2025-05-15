from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class ChatMessage:
    content: str
    sender: str
    sent_at: datetime = field(default_factory=datetime.now)
