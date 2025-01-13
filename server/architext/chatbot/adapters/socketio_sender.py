
import dataclasses
from typing import Mapping
from architext.chatbot.ports.sender import AbstractSender, Message


class SocketIOSender(AbstractSender):
    def __init__(self, sio, user_id_to_socket_id: Mapping[str, str]):
        self.sio = sio
        self.user_id_to_socket_id = user_id_to_socket_id

    def _send(self, user_id: str, message: Message) -> None:
        print("SENDING", message)
        if user_id is not None and user_id in self.user_id_to_socket_id:
            self.sio.emit('chatbot_server_message', dataclasses.asdict(message), to=self.user_id_to_socket_id[user_id])