
import dataclasses
from typing import List
from architext.chatbot.ports.messaging_channel import MessagingChannel, Message
from architext.core.facade import Architext

@dataclasses.dataclass
class SentRecord:
    message: Message
    to_user_id: str

class FakeMessagingChannel(MessagingChannel):
    def __init__(self) -> None:
        self._record: List[SentRecord] = []
        self._last_read_index: int = 0  # Índice del último mensaje leído

    def send(self, user_id: str, message: Message) -> None:
        self._record.append(SentRecord(message, user_id))

    @property
    def all(self) -> str:
        return '\n'.join([record.message.text for record in self._record])

    @property
    def _sent(self) -> List[Message]:
        return [record.message for record in self._record]

    def all_to(self, user_id: str) -> str:
        return '\n'.join([record.message.text for record in self._record if record.to_user_id == user_id])

    @property
    def unread(self) -> str:
        unread_messages = self._record[self._last_read_index:]
        self._last_read_index = len(self._record)
        return '\n'.join(record.message.text for record in unread_messages)

