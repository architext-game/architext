from typing import List, Dict, Callable, Type
from architext.clean.domain.events.events import Event

class MessageBus:
    def __init__(self, handlers: Dict[Type, List[Callable]]):
        self._handlers = handlers

    def handle(self, event: Event):
        for handler in self._handlers.get(type(event), []):
                handler(event)

