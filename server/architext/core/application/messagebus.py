"""
# Messagebus module

 - The `MessageBus` `handle` method drives the `core` module's functionality
 - It will be passed one or more Commands (see `commands` module) and a `UnitOfWork`.
 - For each command handled by the `MessageBus`, it will also handle all events
 reported by the `UnitOfWork`.
 - `Commands` capture intent to change our system from an outside system and .
    - They are stated in imperative mood.
    - They return information on success and prevent other messages from being handled
    if they fail.
 - `Events` capture things that have happened in the system.
    - They are stated in a declarative past way, since they describe things that happened
    in the past.
    - They don't return information on success.
    - They fail silently and don't prevent other events from being handled.
"""

from typing import List, Dict, Callable, Type, TypeVar, Union, Any
from architext.core.domain.events import Event
from architext.core.application.commands.base import Command
from architext.core.application.event_handlers import EVENT_HANDLERS
from architext.core.application.commands import COMMAND_HANDLERS
import logging
from architext.core.application.ports.unit_of_work import UnitOfWork

logger = logging.getLogger(__name__)

Message = Union[Event, Command]

T = TypeVar("T")

class MessageBus:
    """
    - The `MessageBus` `handle` method drives the `core` module's functionality
    - It will be passed one or more Commands (see `commands` module) and a `UnitOfWork`.
    - For each command handled by the `MessageBus`, it will also handle all events
    reported by the `UnitOfWork`.
    - `Commands` capture intent to change our system from an outside system.
        - They are stated in imperative mood.
        - They return information on success.
        - They fail noisily stopping the request and preventing generated events from being handled.
        - Each command has exactly one handler.
    - `Events` capture things that have happened in the system during the handling of commands or other events.
        - They may have zero, one or multiple handlers.
        - They are stated in a declarative past way, since they describe things that happened
        in the past.
        - They don't return information on success.
        - They fail silently with just a log, letting other events be handled.
    """
    def __init__(
            self,
            event_handlers: Dict[Type, List[Callable]] = EVENT_HANDLERS,
            command_handlers: Dict[Type, Callable] = COMMAND_HANDLERS,
        ):
        self._command_handlers = command_handlers
        self._event_handlers = event_handlers

    def handle(self, uow: UnitOfWork, command: Command[T], client_user_id: str = "") -> T:
        """
        Handler for events and commands.
        """
        results = []
        queue: List[Union[Event, Command[Any]]] = [command]
        while queue:
            message = queue.pop(0)
            if isinstance(message, Event):
                self._handle_event(uow, message, queue)
            elif isinstance(message, Command):
                cmd_result = self._handle_command(uow, message, queue, client_user_id)
                results.append(cmd_result)
            else:
                raise Exception(f'{message} was not an Event or Command')
        return results[0]

    def _handle_event(self, uow: UnitOfWork, event: Event, queue: List[Message]):
        for handler in self._event_handlers.get(type(event), []):
            try:
                logger.debug('handling event %s with handler %s', event, handler)
                handler(uow, event)
                queue.extend(uow.collect_new_events())
            except Exception:
                logger.exception('Exception handling event %s', event)
                continue

    def _handle_command(self, uow: UnitOfWork, command: Command, queue: List[Message], client_user_id: str):
        logger.debug('handling command %s', command)
        try:
            handler = self._command_handlers[type(command)]
            result = handler(uow, command, client_user_id)
            queue.extend(uow.collect_new_events())
            return result
        except Exception:
            logger.exception(f"Exception handling command {type(command)} {command}")
            raise

