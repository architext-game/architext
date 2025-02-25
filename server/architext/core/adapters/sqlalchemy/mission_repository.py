from sqlalchemy.orm import Session
from typing import Optional, List
from architext.core.domain.entities.mission import Mission, MissionLog, MissionRequirement
from architext.core.domain.entities.user import User, WorldVisitRecord
from architext.core.ports.mission_repository import MissionRepository
from architext.core.ports.user_repository import UserRepository
from sqlalchemy import Column, DateTime, String, Boolean, ForeignKey, Table, and_, text
from sqlalchemy.orm import relationship
from sqlalchemy.orm.collections import attribute_mapped_collection  # type: ignore

from architext.core.adapters.sqlalchemy.config import metadata, mapper_registry


missions_table = Table(
    "missions", metadata,
    Column("id", String, primary_key=True),
    Column("name", String, nullable=False),
    Column("description", String, nullable=False),
)

mission_requirements_table = Table(
    "mission_requirements", metadata,
    Column("mission_id", String, ForeignKey("missions.id"), primary_key=True),
    Column("complete_mission_with_id", String, ForeignKey("missions.id"), primary_key=True),
)

mission_logs_table = Table(
    "mission_logs", metadata,
    Column("mission_id", String, ForeignKey("missions.id"), primary_key=True),
    Column("user_id", String, ForeignKey("users.id"), primary_key=True),
    Column("completed_at", DateTime, nullable=True),
)


def map_entities():
    mapper_registry.map_imperatively(MissionLog, mission_logs_table)
    mapper_registry.map_imperatively(MissionRequirement, mission_requirements_table)
    mapper_registry.map_imperatively(Mission, missions_table, properties={
        "requirements": relationship(
            MissionRequirement,
            primaryjoin="Mission.id == MissionRequirement.mission_id",
            cascade="all, delete-orphan",
            collection_class=list,
        ),
    })


class SQLAlchemyMissionRepository(MissionRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_mission_by_id(self, mission_id: str) -> Optional[Mission]:
        return self.db_session.query(Mission).filter_by(id=mission_id).first()

    def save_mission(self, mission: Mission) -> None:
        self.db_session.merge(mission)

    def list_missions(self) -> List[Mission]:
        return self.db_session.query(Mission).all()

    def get_mission_log(self, mission_id: str, user_id: str) -> Optional[MissionLog]:
        return self.db_session.query(MissionLog).filter_by(mission_id=mission_id, user_id=user_id).first()

    def list_mission_logs_by_user_id(self, user_id: str) -> List[MissionLog]:
        return self.db_session.query(MissionLog).filter_by(user_id=user_id).all()

    def save_mission_log(self, mission_log: MissionLog) -> None:
        self.db_session.merge(mission_log)
