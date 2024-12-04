from typing import Protocol, Optional, List
from ..entities.room import Room

class RoomRepository(Protocol):
    def get_room_by_id(self, room_id: str) -> Room:
        pass

    def save_room(self, room: Room) -> None:
        pass

    def delete_room(self, room_id: str) -> None:
        pass

    def list_rooms(self) -> List[Room]:
        pass
