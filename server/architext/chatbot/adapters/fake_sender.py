
import dataclasses
from typing import List
from architext.chatbot.ports.sender import AbstractSender, Message
from architext.core.facade import Architext

class FakeSender(AbstractSender):
    def __init__(self, architext: Architext):
        super().__init__(architext)
        self._sent: List[Message] = []
        self._last_read_index: int = 0  # Índice del último mensaje leído

    def _send(self, user_id: str, message: Message) -> None:
        print(dataclasses.asdict(message))
        self._sent.append(message)

    @property
    def last(self) -> Message:
        return self._sent[-1]

    @property
    def all(self) -> str:
        return '\n'.join([message.text for message in self._sent])

    @property
    def unread(self) -> str:
        unread_messages = self._sent[self._last_read_index:]
        self._last_read_index = len(self._sent)
        return '\n'.join(message.text for message in unread_messages)

