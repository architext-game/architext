from typing import List, Dict, Callable, Type
from architext.domain.events.events import Event

class MessageBus:
    def __init__(self, handlers: Dict[Type, List[Callable]]):
        self._handlers = handlers

    def add_handlers(self, handlers: Dict[Type, List[Callable]]):
         for event_type in handlers:
              existing_handlers = self._handlers.get(event_type, [])
              self._handlers[event_type] = existing_handlers + handlers[event_type]

    def handle(self, event: Event) -> None:
        for handler in self._handlers.get(type(event), []):
            try:
                handler(event)
            except Exception as e:
                print(e)

