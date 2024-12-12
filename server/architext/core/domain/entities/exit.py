from dataclasses import dataclass

@dataclass
class Exit:
    """Exits are part of the Room aggregate"""
    name: str
    description: str
    destination_room_id: str
