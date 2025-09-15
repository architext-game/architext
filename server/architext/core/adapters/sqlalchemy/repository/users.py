from sqlalchemy.orm import Session
from typing import Optional, List
from architext.core.domain.entities.user import User, WorldVisitRecord
from architext.core.ports.repository.users import UserRepository
from sqlalchemy import Column, String, Boolean, ForeignKey, Table, and_, text
from sqlalchemy.orm import relationship
from sqlalchemy.orm.collections import attribute_mapped_collection  # type: ignore

from architext.core.adapters.sqlalchemy.config import metadata, mapper_registry


users_table = Table(
    "users", metadata,
    Column("id", String, primary_key=True),
    Column("name", String, nullable=False, unique=True),
    Column("world_id", String, ForeignKey("worlds.id", ondelete="SET NULL"), nullable=True, default=None),
    Column("active", Boolean, nullable=False, server_default=text("false")),
    Column("email", String, nullable=True, default=None, unique=True),
)

world_visit_records_table = Table(
    "world_visit_records", metadata,
    Column("user_id", String, ForeignKey("users.id"), primary_key=True),
    Column("world_id", String, ForeignKey("worlds.id", ondelete="CASCADE"), primary_key=True),
    Column("last_room_id", String, ForeignKey("rooms.id"), nullable=False),
)

def map_entities():
    mapper_registry.map_imperatively(WorldVisitRecord, world_visit_records_table)

    mapper_registry.map_imperatively(User, users_table, properties={
        "world_visit_record": relationship(
            WorldVisitRecord,
            primaryjoin="User.id == WorldVisitRecord.user_id",
            cascade="all, delete-orphan",
            collection_class=attribute_mapped_collection("world_id"),
        )
    })

class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        return self.db_session.query(User).filter_by(id=user_id).first()

    def get_user_by_email(self, user_email: str) -> Optional[User]:
        return self.db_session.query(User).filter_by(email=user_email).first()

    def get_user_by_name(self, username: str) -> Optional[User]:
        return self.db_session.query(User).filter_by(name=username).first()

    def save_user(self, user: User) -> None:
        self.db_session.merge(user)

    def delete_user(self, user_id: str) -> None:
        self.db_session.query(User).filter_by(id=user_id).delete()

    def list_users(self) -> List[User]:
        return self.db_session.query(User).all()

    def get_users_in_room(self, room_id: str) -> List[User]:
        return (
            self.db_session.query(User)
            .join(WorldVisitRecord, onclause=(and_(
                users_table.c.id == world_visit_records_table.c.user_id,
                users_table.c.world_id == world_visit_records_table.c.world_id
            )))
            .filter_by(last_room_id=room_id)
            .all()
        )
