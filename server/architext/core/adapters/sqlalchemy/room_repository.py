from typing import List, Optional
from architext.core.domain.entities.exit import Exit
from architext.core.domain.entities.item import Item
from architext.core.domain.entities.room import Room
from architext.core.ports.room_repository import RoomRepository
from sqlalchemy.orm import Session
from typing import Optional, List
from sqlalchemy import Column, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.orm.collections import attribute_mapped_collection  # type: ignore

from architext.core.adapters.sqlalchemy.config import metadata, mapper_registry

rooms_table = Table(
    "rooms", metadata,
    Column("id", String, primary_key=True),
    Column("name", String, nullable=False),
    Column("world_id", String, ForeignKey("worlds.id", deferrable=True, initially="DEFERRED", ondelete="CASCADE"), nullable=False),
    Column("description", String, nullable=False, default=""),
)

exits_table = Table(
    "exits", metadata,
    Column("room_id", String, ForeignKey("rooms.id", deferrable=True, initially="DEFERRED", ondelete="CASCADE"), primary_key=True),
    Column("name", String, nullable=False, primary_key=True),
    Column("description", String, nullable=False, default=""),
    Column("destination_room_id", String, ForeignKey("rooms.id", deferrable=True, initially="DEFERRED", ondelete="CASCADE")),
    Column("visibility", String, nullable=False),
)

items_table = Table(
    "items", metadata,
    Column("room_id", String, ForeignKey("rooms.id", deferrable=True, initially="DEFERRED", ondelete="CASCADE"), primary_key=True),
    Column("name", String, nullable=False, primary_key=True),
    Column("description", String, nullable=False, default=""),
    Column("visibility", String, nullable=False),
)

def map_entities():
    mapper_registry.map_imperatively(Exit, exits_table)
    mapper_registry.map_imperatively(Item, items_table)

    mapper_registry.map_imperatively(Room, rooms_table, properties={
        "exits": relationship(
            Exit,
            primaryjoin="Room.id == Exit.room_id",
            cascade="all, delete-orphan",
            collection_class=attribute_mapped_collection("name"),
        ),
        "items": relationship(
            Item,
            primaryjoin="Room.id == Item.room_id",
            cascade="all, delete-orphan",
            collection_class=attribute_mapped_collection("name"),
        )
    })

class SQLAlchemyRoomRepository(RoomRepository):
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    def get_room_by_id(self, room_id: str) -> Optional[Room]:
        return self.db_session.query(Room).filter_by(id=room_id).one_or_none()

    def save_room(self, room: Room) -> None:
        self.db_session.merge(room)

    def delete_room(self, room_id: str) -> None:
        self.db_session.query(Room).filter_by(id=room_id).delete()

    def delete_all_exits_leading_to_room(self, room_id: str) -> None:
        self.db_session.query(Exit).filter_by(destination_room_id=room_id).delete()

    def list_rooms(self) -> List[Room]:
        return list(self.db_session.query(Room))
    
    def list_rooms_by_world(self, world_id: str) -> List[Room]:
        return list(self.db_session.query(Room).filter_by(world_id=world_id))
