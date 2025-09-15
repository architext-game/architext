from architext.core.adapters.fake.uow import FakeUnitOfWork
from architext.core.domain.entities.world import World
from architext.core.domain.entities.world_template import WorldTemplate
from architext.core.queries.list_world_templates import ListWorldTemplates
from architext.core.queries.list_worlds import ListWorlds
import pytest # type: ignore
from architext.core.domain.entities.room import Room
from architext.core import Architext
import pprint


def test_list_world_templates(architext: Architext):
    out = architext.query(ListWorldTemplates(), "oliver")
    pprint.pprint(out.templates)
    assert len(out.templates) == 4

    # A public template I don't own should be on the list
    assert next((world for world in out.templates if world.id == "emptytemplate"), None) is not None
    # A public template I own should be on the list
    assert next((world for world in out.templates if world.id == "braggingtemplate"), None) is not None
    # A private template I don't own should not be on the list
    assert next((world for world in out.templates if world.id == "rabbittemplate"), None) is None
    # A private template I own should be on the list
    templateforme = next((world for world in out.templates if world.id == "templateforme"), None)
    assert templateforme is not None
    assert templateforme.id == "templateforme"
    assert templateforme.description == "For the new worlds I create"
