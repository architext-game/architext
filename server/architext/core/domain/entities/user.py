from typing import Dict, Optional, Set
from dataclasses import dataclass, field
import hashlib

@dataclass
class WorldVisitRecord:
    world_id: str
    last_room_id: str

@dataclass
class User:
    id: str
    name: str
    password_hash: bytes
    world_id: Optional[str] = None
    active: bool = False
    email: Optional[str] = None
    world_visit_record: Dict[str, WorldVisitRecord] = field(default_factory=dict)

    @property
    def room_id(self) -> Optional[str]:
        print("ROOM ID CHECK for user", self.name, self.world_id)
        if self.world_id is None:
            return None
        return self.world_visit_record[self.world_id].last_room_id

    @property
    def visited_world_ids(self) -> Set[str]:
        return {record.world_id for record in self.world_visit_record.values()}

    def set_room(self, room_id: str, world_id: str) -> None:
        """Changes the current room of the user and updates the world visit record"""
        world_record = self.world_visit_record.get(world_id, None)
        if world_record is None:
            self.world_visit_record[world_id] = WorldVisitRecord(
                world_id=world_id,
                last_room_id=room_id,
            )
        else:
            world_record.last_room_id=room_id
        self.world_id = world_id

    def _hash_password(self, password: str) -> bytes:
        """Hashes a password using SHA-256."""
        return hashlib.sha256(password.encode('utf-8')).digest()

    def match_password(self, password: str) -> bool:
        """Checks if the provided password matches the stored hash."""
        return self.password_hash == self._hash_password(password)

