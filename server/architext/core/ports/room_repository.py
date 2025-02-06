from typing import Protocol, List, Optional
from architext.core.domain.entities.room import Room

class RoomRepository(Protocol):
    def get_room_by_id(self, room_id: str) -> Optional[Room]:
        pass

    def save_room(self, room: Room) -> None:
        pass

    def delete_room(self, room_id: str) -> None:
        pass

    def delete_all_exits_leading_to_room(self, room_id: str) -> None:
        pass

    def list_rooms(self) -> List[Room]:
        pass

    def list_rooms_by_world(self, world_id: str) -> List[Room]:
        pass
