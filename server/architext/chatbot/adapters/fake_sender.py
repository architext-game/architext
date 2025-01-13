
import dataclasses
from architext.chatbot.ports.sender import AbstractSender, Message

class FakeSender(AbstractSender):
    def __init__(self):
        self._sent = []

    def _send(self, user_id: str, message: Message) -> None:
        print(dataclasses.asdict(message))
        self._sent.append(message)
