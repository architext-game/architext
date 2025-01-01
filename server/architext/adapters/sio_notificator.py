from typing import List, Mapping
from architext.ports.notificator import Notificator, JSONSerializable
from dataclasses import dataclass
from socketio import Server as SocketIOServer

@dataclass
class NotificationRecord:
    user_id: str
    event: str
    data: object

class SocketIONotificator(Notificator):
    def __init__(self, sio: SocketIOServer, user_id_to_socket_id: Mapping[str, str]) -> None:
        self.notifications: Mapping[str, List] = {}
        self._user_id_to_socket_id = user_id_to_socket_id
        self._sio = sio

    def notify_user(self, user_id: str, event: str, data: JSONSerializable):
        if user_id in self._user_id_to_socket_id:
            self._sio.emit(event, data, self._user_id_to_socket_id[user_id])


