from typing import List, Optional
from architext.core.domain.entities.world import World
from architext.core.ports.repository.worlds import WorldRepository
from sqlalchemy.orm import Session
from typing import Optional, List
from sqlalchemy import Column, ForeignKey, String, Table
from architext.core.adapters.sqlalchemy.config import metadata, mapper_registry


worlds_table = Table(
    "worlds", metadata,
    Column("id", String, primary_key=True),
    Column("name", String, nullable=False),
    Column("description", String, nullable=False, default=""),
    Column("initial_room_id", String, ForeignKey("rooms.id", deferrable=True, initially="DEFERRED"), nullable=False),
    Column("owner_user_id", String, ForeignKey("users.id"), nullable=True),
    Column("visibility", String, nullable=False, default="private"),
    Column("base_template_id", String, ForeignKey("world_templates.id", ondelete="SET NULL"), nullable=True),
)

def map_entities():
    mapper_registry.map_imperatively(World, worlds_table)


class SQLAlchemyWorldRepository(WorldRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_world_by_id(self, world_id: str) -> Optional[World]:
        return self.db_session.query(World).filter_by(id=world_id).one_or_none()

    def save_world(self, world: World) -> None:
        self.db_session.merge(world)

    def delete_world(self, world_id: str) -> None:
        self.db_session.query(World).filter_by(id=world_id).delete()

    def list_worlds(self) -> List[World]:
        return self.db_session.query(World).all()
