from typing import TYPE_CHECKING, Union, Mapping, Iterable, List

from architext.core.domain.events import Event
from architext.core.ports.external_event_publisher import ExternalEventPublisher

if TYPE_CHECKING:
    from architext.core.ports.unit_of_work import UnitOfWork
else:
    UnitOfWork = object()

JSONSerializable = Union[str, int, float, bool, None, Mapping[str, 'JSONSerializable'], Iterable['JSONSerializable']]

class FakeExternalEventPublisher(ExternalEventPublisher):
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow
        self.published_events: List[Event] = []
    
    def publish(self, event: Event):
        # idea: handle external events as internal in testing
        # would need to setup handlers in a way that does not make sense
        # for production
        self.uow.publish_events([event])
        self.published_events.append(event)
