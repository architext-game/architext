import os
from typing import Literal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from architext.core.adapters.sqlalchemy import user_repository
from architext.core.adapters.sqlalchemy import room_repository
from architext.core.adapters.sqlalchemy import world_repository
from architext.core.adapters.sqlalchemy import world_template_repository
from architext.core.adapters.sqlalchemy import mission_repository
from architext.core.adapters.sqlalchemy.config import metadata
from sqlalchemy.orm import clear_mappers

def db_connection(at: Literal['memory', 'file', 'url'] = 'memory', url: str = "", filename: str = "database.db") -> sessionmaker:
    if at == "memory":
        engine = create_engine("sqlite:///:memory:", echo=False)
    elif at == "file":
        engine = create_engine(f"sqlite:///{filename}", echo=False)
    elif at == "url":
        engine = create_engine(url)

    session_factory = sessionmaker(engine)
    clear_mappers()
    user_repository.map_entities()
    room_repository.map_entities()
    world_repository.map_entities()
    world_template_repository.map_entities()
    mission_repository.map_entities()
    metadata.create_all(engine)
    return session_factory