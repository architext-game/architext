
import dataclasses
from typing import Mapping
from architext.chatbot.ports.messaging_channel import MessagingChannel, Message


class SocketIOMessagingChannel(MessagingChannel):
    def __init__(self, sio, user_id_to_socket_id: Mapping[str, str]):
        self.sio = sio
        self.user_id_to_socket_id = user_id_to_socket_id

    def send(self, user_id: str, message: Message) -> None:
        if user_id is not None and user_id in self.user_id_to_socket_id:
            self.sio.emit('chatbot_server_message', dataclasses.asdict(message), to=self.user_id_to_socket_id[user_id])