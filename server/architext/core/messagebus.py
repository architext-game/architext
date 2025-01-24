"""
# Messagebus module

 - This is the facade of the `core` module, along with the `commands` module.
 - The `MessageBus` `handle` method is the method used by external systems to
 drive the `core` module.
 - It will be passed one or more Commands (see `commands` module) and a `UnitOfWork`.
 - For each command handled by the `MessageBus`, it will also handle all events
 reported by the `UnitOfWork`.
 - Commands and events are different concepts and handled differently.
 - Commands capture intent to change our system from an outside system.
 - They are stated in imperative mood.
 - They return information on success and prevent other messages from being handled
 if they fail.
 - Events capture things that have happened in the system.
 - They are stated in a declarative past way.
 - They don't return information on success.
 - They fail silently and don't prevent other events from being handled.
"""

from typing import List, Dict, Callable, Type, TypeVar, Union, Any
from architext.core.domain.events import Event
from architext.core.commands import Command
from architext.core.handlers import EVENT_HANDLERS
from architext.core.services import COMMAND_HANDLERS
import logging
from architext.core.ports.unit_of_work import UnitOfWork

logger = logging.getLogger(__name__)

Message = Union[Event, Command]

T = TypeVar("T")

class MessageBus:
    def __init__(
            self,
            event_handlers: Dict[Type, List[Callable]] = EVENT_HANDLERS,
            command_handlers: Dict[Type, Callable] = COMMAND_HANDLERS
        ):
        self._event_handlers = event_handlers
        self._command_handlers = command_handlers

    def handle(self, uow: UnitOfWork, command: Command[T], client_user_id: str = "") -> T:
        """
        Handler for events and commands. Both are handled a bit differently:
        - Commands: Fail noisily stopping the request and notify on success.
            Each command has a single known handler.
        - Events: Fail silently with just a log. Let other events execute.
            Each event may have zero or multiple handlers.
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

