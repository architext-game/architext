from typing import Protocol

from typing import Any, Union, Mapping, Iterable

JSONSerializable = Union[str, int, float, bool, None, Mapping[str, 'JSONSerializable'], Iterable['JSONSerializable']]

class Notificator(Protocol):
    def notify_user(self, user_id: str, event: str, data: JSONSerializable):
        pass
