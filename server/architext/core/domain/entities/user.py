from typing import Mapping, Optional, Set
from dataclasses import dataclass, field
import hashlib

@dataclass(frozen=True)
class WorldVisitRecord:
    world_id: str
    last_room_id: str

    def with_changes(self, last_room_id: Optional[str] = None):
        return WorldVisitRecord(
            world_id=self.world_id,
            last_room_id=last_room_id if last_room_id else self.last_room_id,
        )

@dataclass(frozen=True)
class User:
    id: str
    name: str
    password_hash: bytes
    world_id: Optional[str] = None
    active: bool = False
    email: Optional[str] = None
    world_visit_record: Mapping[str, WorldVisitRecord] = field(default_factory=dict)

    @property
    def room_id(self) -> Optional[str]:
        print("ROOM ID CHECK for user", self.name, self.world_id)
        if self.world_id is None:
            return None
        return self.world_visit_record[self.world_id].last_room_id

    @property
    def visited_world_ids(self) -> Set[str]:
        return {record.world_id for record in self.world_visit_record.values()}

    def with_current_room(self, room_id: str, world_id: str) -> "User":
        that_world_record = self.world_visit_record.get(world_id, None)
        if that_world_record is None:
            updated_record = WorldVisitRecord(
                world_id=world_id,
                last_room_id=room_id,
            )
        else:
            updated_record = that_world_record.with_changes(last_room_id=room_id)
        new_visit_record = dict(self.world_visit_record)
        new_visit_record[world_id] = updated_record

        return self.with_changes(
            world_id=world_id,
            world_visit_record=new_visit_record
        )

    def _hash_password(self, password: str) -> bytes:
        """Hashes a password using SHA-256."""
        return hashlib.sha256(password.encode('utf-8')).digest()

    def match_password(self, password: str) -> bool:
        """Checks if the provided password matches the stored hash."""
        return self.password_hash == self._hash_password(password)

    def with_changes(
        self, 
        active: Optional[bool] = None,
        world_id: Optional[str] = None,
        world_visit_record: Optional[Mapping[str, WorldVisitRecord]] = None,
    ) -> "User":
        return User(
            active=active if active is not None else self.active,
            world_id=world_id if world_id is not None else self.world_id,
            id=self.id,
            name=self.name,
            email=self.email,
            password_hash=self.password_hash,
            world_visit_record=world_visit_record if world_visit_record is not None else self.world_visit_record,
        )
