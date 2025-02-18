import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from architext.core.adapters.sqlalchemy import user_repository
from architext.core.adapters.sqlalchemy import room_repository
from architext.core.adapters.sqlalchemy import world_repository
from architext.core.adapters.sqlalchemy import world_template_repository
from architext.core.adapters.sqlalchemy.config import metadata
from sqlalchemy.orm import clear_mappers

def db_connection() -> sessionmaker:
    engine = create_engine("sqlite:///:memory:", echo=False)
    # engine = create_engine("sqlite:///database.db", echo=False)
    session_factory = sessionmaker(engine)
    clear_mappers()
    user_repository.map_entities()
    room_repository.map_entities()
    world_repository.map_entities()
    world_template_repository.map_entities()
    metadata.create_all(engine)
    return session_factory