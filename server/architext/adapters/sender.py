import abc
from architext.adapters.repository import AbstractRepository
import typing

"""
Métodos de enviar que estaban en la sesión
def send_to_client(self, message):
        self.send(self.client_id, "\n\r"+message)
        if self.logger:
            self.logger.info('server\n'+message)

def send_to_user(self, user, message):
    if user.client_id is not None:
        self.send(user.client_id, "\n\r"+message)

def send_to_room_except(self, exception_user, message):
    users_in_this_room = entities.User.objects(room=self.user.room)
    for user in users_in_this_room:
        if user != exception_user:
            self.send(user.client_id, message)

def send_to_others_in_room(self, message):
    self.send_to_room_except(self.user, message)

def send_to_room(self, message):
    users_in_this_room = entities.User.objects(room=self.user.room)
    for user in users_in_this_room:
        self.send(user.client_id, message)

def send_to_all(self, message):
    for user in entities.User.objects:
        self.send(user.client_id, message)

def send(self, client_id, message):
    # Wrap the message to 80 characters
    message = '\n'.join(
        # Wrap each line individually
        ['\n'.join(textwrap.wrap(line, 80,
            replace_whitespace=False,
            expand_tabs=False,
            drop_whitespace=False,
            break_on_hyphens=False,
            break_long_words=False
            ))
        for line in message.splitlines()]
    )

    self.server.send_message(client_id, message)
"""

class AbstractSender(abc.ABC):
    @abc.abstractmethod
    def send_to_client(self, message: str) -> None:
        pass

    @abc.abstractmethod
    def send_to_others_in_room(self, message: str) -> None:
        pass

class FakeSender(AbstractSender):
    def __init__(self):
        self._sent = []

    def send_to_client(self, message: str) -> None:
        print(message)
        self._sent.append(('client', message))

    def send_to_others_in_room(self, message: str) -> None:
        print(message)
        self._sent.append(('room', message))

class SocketIOSender(AbstractSender):
    def __init__(self, socket_id, repository: AbstractRepository, sio):
        self.socket_id = socket_id
        self.repository = repository
        self.sio = sio

    def send_to_client(self, message: str) -> None:
        self._send(self.socket_id, message)

    def send_to_others_in_room(self, message: str) -> None:
        user = self.repository.get_user_by_connection(self.socket_id)
        avatar = self.repository.get_active_avatar_of_user(user.id)
        users = self.repository.get_users_in_room(avatar.current_room_id)
        for user in users:
            if user.connection_id:
                self._send(user.connection_id, message)

    def _send(self, socket_id, message):
        self.sio.emit('message', message, to=socket_id)

