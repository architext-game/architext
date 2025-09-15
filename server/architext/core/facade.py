"""
# Facade module

This module defines the interface of the core module. All users of the core
should interact with it only through the Architext class defined below.
"""

from typing import TypeVar
from architext.core.authorization import AuthorizationManager
from architext.core.commands import Command
from architext.core.messagebus import MessageBus
from architext.core.ports.unit_of_work import UnitOfWork
from architext.core.queries.base import Query

T = TypeVar("T")

class Architext:
    """
    This class exposes the core functionality of the game.
    - Drive the game's functionality by handling commands using the `handle` method.
    - Query the game's state passing queries to the `query` method.
    """
    def __init__(self, uow: UnitOfWork):
        self._uow = uow
        self._messagebus = MessageBus()
        self.authorization = AuthorizationManager(uow)

    def handle(self, command: Command[T], client_user_id: str = "") -> T:
        """Handles a command (i.e. a request to modify the state of the game)
        and returns its result."""
        return self._messagebus.handle(self._uow, command, client_user_id)

    def query(self, query: Query[T], client_user_id: str = "") -> T:
        """Handles a query (i.e. a request for specific information from the
        state of the game without any side effects) and returns its result."""
        return self._uow.queries.query(query, client_user_id)
