import os
from typing import Literal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from architext.core.adapters.sqlalchemy.repository import users
from architext.core.adapters.sqlalchemy.repository import rooms
from architext.core.adapters.sqlalchemy.repository import worlds
from architext.core.adapters.sqlalchemy.repository import world_templates
from architext.core.adapters.sqlalchemy.repository import missions
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
    users.map_entities()
    rooms.map_entities()
    worlds.map_entities()
    world_templates.map_entities()
    missions.map_entities()
    metadata.create_all(engine)
    return session_factory