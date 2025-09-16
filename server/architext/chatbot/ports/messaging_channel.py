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

class MessagingChannel(abc.ABC):
    @abc.abstractmethod
    def send(self, user_id: str, message: Message) -> None:
        pass

