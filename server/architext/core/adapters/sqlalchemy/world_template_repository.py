from typing import List, Optional
from architext.core.domain.entities.world_template import WorldTemplate
from architext.core.ports.world_template_repository import WorldTemplateRepository
from typing import List, Optional
from sqlalchemy.orm import Session
from typing import Optional, List
from sqlalchemy import Column, String, Table
from architext.core.adapters.sqlalchemy.config import metadata, mapper_registry

world_templates_table = Table(
    "world_templates", metadata,
    Column("id", String, primary_key=True),
    Column("name", String, nullable=False),
    Column("description", String, nullable=False, default=""),
    Column("world_encoded_json", String, nullable=False),
    Column("author_id", String, nullable=True),

    Column("visibility", String, nullable=False, default="private"),
    Column("base_template_id", String, nullable=True),
)

def map_entities():
    mapper_registry.map_imperatively(WorldTemplate, world_templates_table)


class SQLAlchemyWorldTemplateRepository(WorldTemplateRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_world_template_by_id(self, world_template_id: str) -> Optional[WorldTemplate]:
        return self.db_session.query(WorldTemplate).filter_by(id=world_template_id).one_or_none()

    def save_world_template(self, world_template: WorldTemplate) -> None:
        self.db_session.merge(world_template)

    def delete_world_template(self, world_template_id: str) -> None:
        self.db_session.query(WorldTemplate).filter_by(id=world_template_id).delete()

    def list_world_templates(self) -> List[WorldTemplate]:
        return self.db_session.query(WorldTemplate).all()
