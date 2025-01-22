from architext.core.adapters.fake_uow import FakeUnitOfWork
from architext.core.commands import CreateInitialData, CreateTemplate, ImportWorld
from architext.core.domain.entities.exit import Exit
from architext.core.domain.entities.user import User
from architext.core.domain.entities.world import World
from architext.core.queries.world_to_text import WorldToText
import pytest # type: ignore
from architext.core.domain.entities.room import Room
from architext.core import Architext

from test.fixtures import createTestData


@pytest.fixture
def architext() -> Architext:
    return createTestData()


def test_create_template_success(architext: Architext):
    create_template_result = architext.handle(CreateTemplate(
        name="My new template",
        description="I just made this template",
        base_world_id="outer"
    ), client_user_id="oliver")
    template = architext._uow.world_templates.get_world_template_by_id(create_template_result.template_id)
    assert template is not None
    original_text = architext.query(WorldToText(world_id="outer", format="encoded"), client_user_id="oliver").text_representation
    assert template.world_encoded_json == original_text
    assert template.author_id == "oliver"
    assert template.name == "My new template"
    assert template.description == "I just made this template"


def test_unauthorized_user_cant_create_template(architext: Architext):
    with pytest.raises(PermissionError):
        architext.handle(CreateTemplate(
            name="My new template",
            description="I just made this template",
            base_world_id="outer"
        ), client_user_id="alice")


    
    