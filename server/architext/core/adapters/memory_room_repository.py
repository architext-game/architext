from typing import Dict, List, Optional
from architext.core.domain.entities.room import Room
from architext.core.ports.room_repository import RoomRepository
from copy import deepcopy


class MemoryRoomRepository(RoomRepository):
    def __init__(self) -> None:
        self._rooms: Dict[str, Room] = {}

    def get_room_by_id(self, room_id: str) -> Optional[Room]:
        return self._rooms.get(room_id, None)

    def save_room(self, room: Room) -> None:
        self._rooms[room.id] = room

    def delete_room(self, room_id: str) -> None:
        del self._rooms[room_id]

    def list_rooms(self) -> List[Room]:
        return list(self._rooms.values())
    
    def list_rooms_by_world(self, world_id: str) -> List[Room]:
        return [room for room in self._rooms.values() if room.world_id == world_id]
