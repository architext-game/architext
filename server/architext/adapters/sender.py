import abc
import typing

class AbstractSender(abc.ABC):
    @abc.abstractmethod
    def send(self, connection_id: str, message: str) -> None:
        pass

class FakeSender(AbstractSender):
    def __init__(self):
        self._sent = []

    def send(self, connection_id: str, message: str) -> None:
        print(message)
        self._sent.append(('client', message))

class SocketIOSender(AbstractSender):
    def __init__(self, sio):
        self.sio = sio

    def send(self, socket_id, message):
        self.sio.emit('message', message, to=socket_id)

