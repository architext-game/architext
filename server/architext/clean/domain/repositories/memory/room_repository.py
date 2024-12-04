from typing import Dict, List
from architext.clean.domain.entities.room import Room
from architext.clean.domain.repositories.room_repository import RoomRepository
import copy

class MemoryRoomRepository(RoomRepository):
    _rooms: Dict[str, Room] = {}

    def get_room_by_id(self, room_id: str) -> Room:
        return self._rooms[room_id]

    def save_room(self, room: Room) -> None:
        self._rooms[room.id] = room

    def delete_room(self, room_id: str) -> None:
        del self._rooms[room_id]

    def list_rooms(self) -> List[Room]:
        return copy.deepcopy(list(self._rooms.values()))
