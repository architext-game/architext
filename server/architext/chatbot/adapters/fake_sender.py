
import dataclasses
from typing import List
from architext.chatbot.ports.sender import AbstractSender, Message
from architext.core.facade import Architext

class FakeSender(AbstractSender):
    def __init__(self, architext: Architext):
        super().__init__(architext)
        self._sent: List[Message] = []

    def _send(self, user_id: str, message: Message) -> None:
        print(dataclasses.asdict(message))
        self._sent.append(message)
