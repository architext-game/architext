from typing import List, Optional, Set
from dataclasses import dataclass, field
import hashlib

@dataclass
class User:
    id: str
    name: str
    password_hash: bytes
    room_id: Optional[str] = None
    email: Optional[str] = None
    visited_world_ids: Set[str] = field(default_factory=set)

    def _hash_password(self, password: str) -> bytes:
        """Hashes a password using SHA-256."""
        return hashlib.sha256(password.encode('utf-8')).digest()

    def set_password(self, password: str) -> None:
        """Sets the password hash for the user."""
        self.password_hash = self._hash_password(password)

    def match_password(self, password: str) -> bool:
        """Checks if the provided password matches the stored hash."""
        return self.password_hash == self._hash_password(password)
