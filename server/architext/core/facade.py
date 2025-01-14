

from typing import Optional, TypeVar
from architext.core.commands import Command
from architext.core.messagebus import MessageBus
from architext.core.ports.unit_of_work import UnitOfWork

T = TypeVar("T")

class Architext:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow
        self._messagebus = MessageBus()

    def handle(self, command: Command[T], client_user_id: str = "") -> T:
        return self._messagebus.handle(self._uow, command, client_user_id)