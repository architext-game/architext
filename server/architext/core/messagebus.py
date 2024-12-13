from typing import List, Dict, Callable, Type, Union
from architext.core.domain.events import Event
from architext.core.commands import Command
from architext.core.handlers import EVENT_HANDLERS
from architext.core.services import COMMAND_HANDLERS
import logging
from architext.ports.unit_of_work import UnitOfWork

logger = logging.getLogger(__name__)

Message = Union[Event, Command]

class MessageBus:
    def __init__(
            self,
            event_handlers: Dict[Type, List[Callable]] = EVENT_HANDLERS,
            command_handlers: Dict[Type, Callable] = COMMAND_HANDLERS
        ):
        self._event_handlers = event_handlers
        self._command_handlers = command_handlers

    def handle(self, uow: UnitOfWork, message: Message, client_user_id: str = "") -> List:
        """
        Handler for events and commands. Both are handled a bit differently:
        - Commands: Fail noisily stopping the request and notify on success.
            Each command has a single known handler.
        - Events: Fail silently with just a log. Let other events execute.
            Each event may have zero or multiple handlers.
        """
        results = []
        queue = [message]
        while queue:
            message = queue.pop(0)
            if isinstance(message, Event):
                self.handle_event(uow, message, queue)
            elif isinstance(message, Command):
                cmd_result = self.handle_command(uow, message, queue, client_user_id)
                results.append(cmd_result)
            else:
                raise Exception(f'{message} was not an Event or Command')
        return results

    def handle_event(self, uow: UnitOfWork, event: Event, queue: List[Message]):
        for handler in self._event_handlers.get(type(event), []):
            try:
                logger.debug('handling event %s with handler %s', event, handler)
                handler(uow, event)
                queue.extend(uow.collect_new_events())
            except Exception:
                logger.exception('Exception handling event %s', event)
                continue

    def handle_command(self, uow: UnitOfWork, command: Command, queue: List[Message], client_user_id: str):
        logger.debug('handling command %s', command)
        try:
            handler = self._command_handlers[type(command)]
            result = handler(uow, command, client_user_id)
            queue.extend(uow.collect_new_events())
            return result
        except Exception:
            logger.exception('Exception handling command %s', command)
            raise

