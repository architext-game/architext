import abc
import typing
import dataclasses

@dataclasses.dataclass
class MessageOptions():
    display: typing.Literal['wrap', 'box', 'underline', 'fit'] = 'wrap'
    section: bool = True
    fillInput: typing.Optional[str] = None
    asksForPassword: bool = False

@dataclasses.dataclass
class Message():
    text: str
    options: MessageOptions

class AbstractSender(abc.ABC):
    @abc.abstractmethod
    def send(self, connection_id: str, message: Message) -> None:
        pass

class FakeSender(AbstractSender):
    def __init__(self):
        self._sent = []

    def send(self, connection_id: str, message: Message) -> None:
        print(dataclasses.asdict(message))
        self._sent.append(message)

class SocketIOSender(AbstractSender):
    def __init__(self, sio):
        self.sio = sio

    def send(self, connection_id: str, message: Message) -> None:
        if connection_id is not None:
            print(dataclasses.asdict(message))
            self.sio.emit('message', dataclasses.asdict(message), to=connection_id)