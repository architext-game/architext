import abc
import typing
import dataclasses
import textwrap

from architext.core.facade import Architext
from architext.core.messagebus import MessageBus
from architext.core.ports.unit_of_work import UnitOfWork
from architext.core.queries.get_current_room import GetCurrentRoom
from architext.chatbot import strings

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

