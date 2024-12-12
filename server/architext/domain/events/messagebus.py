from typing import List, Dict, Callable, Type, TYPE_CHECKING
from architext.domain.events.events import Event, HANDLERS
if TYPE_CHECKING:
    from architext.domain.unit_of_work.unit_of_work import UnitOfWork
else:
    UnitOfWork = object

class MessageBus:
    def __init__(self, handlers: Dict[Type, List[Callable]] = HANDLERS):
        self._handlers = handlers

    def add_handlers(self, handlers: Dict[Type, List[Callable]]):
         for event_type in handlers:
              existing_handlers = self._handlers.get(event_type, [])
              self._handlers[event_type] = existing_handlers + handlers[event_type]

    def handle(self, uow: UnitOfWork, event: Event) -> None:
        for handler in self._handlers.get(type(event), []):
            try:
                handler(uow, event)
            except Exception as e:
                print(e)

