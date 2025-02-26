from typing import cast
import pytest # type: ignore
from architext.core.adapters.fake_uow import FakeUnitOfWork
from architext.core.adapters.sqlalchemy.uow import SQLAlchemyUnitOfWork
from architext.core.commands import CreateUser, CreateUserResult, Setup
from pydantic import ValidationError
from architext.core import Architext

from architext.core.adapters.fake_uow import FakeUnitOfWork
from architext.core.domain.entities.mission import default_missions
from test.fixtures import createTestArchitext

from uuid import uuid4

@pytest.fixture
def architext() -> Architext:
    return Architext(uow=FakeUnitOfWork())

def test_setup_command_populates_initial_data(architext: Architext):
    architext.handle(Setup())
    uow = architext._uow
    with uow:
        assert len(uow.worlds.list_worlds()) == 1
        assert uow.worlds.get_world_by_id(world_id="monks_riddle") is not None
        assert len(uow.world_templates.list_world_templates()) == 1
        assert uow.world_templates.get_world_template_by_id(world_template_id="empty_template") is not None
        for mission in default_missions().all:
            assert uow.missions.get_mission_by_id(mission.id) is not None


def test_setup_command_is_idempotent(architext: Architext):
    architext.handle(Setup())
    architext.handle(Setup())
    uow = architext._uow
    with uow:
        assert len(uow.worlds.list_worlds()) == 1
        assert len(uow.world_templates.list_world_templates()) == 1
        assert len(uow.missions.list_missions()) == len(default_missions().all)
        

def test_tutorial_world_is_created_for_each_user(architext: Architext):
    command = CreateUser(
        id=str(uuid4()),
        name="John Doe",
        email="john.doe@example.com",
        password="securepassword123"
    )
    architext.handle(command)

    command = CreateUser(
        id=str(uuid4()),
        name="Jane Doe",
        email="jane.doe@example.com",
        password="securepassword123"
    )
    architext.handle(command)

    with architext._uow:
        assert len(architext._uow.users.list_users()) == 2
        assert len(architext._uow.worlds.list_worlds()) == 2

