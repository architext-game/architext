from typing import Dict, List, Optional
from architext.core.domain.entities.room import Room
from architext.core.ports.room_repository import RoomRepository
from copy import deepcopy


class MemoryRoomRepository(RoomRepository):
    def __init__(self) -> None:
        self._rooms: Dict[str, Room] = {}

    def get_room_by_id(self, room_id: str) -> Optional[Room]:
        return deepcopy(self._rooms.get(room_id, None))

    def save_room(self, room: Room) -> None:
        self._rooms[room.id] = deepcopy(room)

    def delete_room(self, room_id: str) -> None:
        del self._rooms[room_id]

    def list_rooms(self) -> List[Room]:
        return deepcopy(list(self._rooms.values()))
