from typing import Protocol

from typing import Union, Mapping, Iterable

from architext.core.domain.events import Event

JSONSerializable = Union[str, int, float, bool, None, Mapping[str, 'JSONSerializable'], Iterable['JSONSerializable']]

class ExternalEventPublisher(Protocol):
    def publish(self, event: Event):
        ...
