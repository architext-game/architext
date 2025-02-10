from dataclasses import dataclass
import dataclasses
from typing import Iterable, List, Mapping, Protocol, Union
from architext.core.ports.notifier import Notifier, Notification
from socketio import Server
import re

def sio_event_name(notification: Notification) -> str:
    """Convert PascalCase or camelCase to snake_case."""
    name = notification.__class__.__name__
    name = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', name)
    name = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', name)
    return name.lower()

@dataclass
class SentRecord:
    to_user_id: str
    notification: Notification

class SioNotifier(Notifier):
    def __init__(self, sio: Server, user_id_to_socket_id: Mapping[str, str]) -> None:
        self.sio = sio
        self.user_id_to_socket_id = user_id_to_socket_id

    def notify(self, user_id: str, notification: Notification) -> None:
        self.sio.emit(
            sio_event_name(notification),
            dataclasses.asdict(notification),
            to=self.user_id_to_socket_id[user_id]
        )