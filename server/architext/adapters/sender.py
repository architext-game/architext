import abc
import typing
import dataclasses

@dataclasses.dataclass
class MessageOptions():
    display: typing.Literal['wrap', 'box', 'underline', 'fit'] = 'wrap'
    section: bool = True

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

    def send(self, socket_id, message, options: MessageOptions = MessageOptions()):
        if socket_id is not None:
            self.sio.emit('message', (message, dataclasses.asdict(options)), to=socket_id)

