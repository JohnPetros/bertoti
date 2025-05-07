from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class ChatMessage:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    company_id: str
    user_id: str
    sender: str
    message: str
    timestamp: datetime = field(default_factory=datetime.now)
