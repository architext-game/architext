from architext.core.adapters.fake_uow import FakeUnitOfWork
from architext.core.commands import CreateInitialData
from architext.core.domain.entities.world import World
from architext.core.domain.entities.world_template import WorldTemplate
from architext.core.queries.list_world_templates import ListWorldTemplates
from architext.core.queries.list_worlds import ListWorlds
import pytest # type: ignore
from architext.core.domain.entities.room import Room
from architext.core import Architext


@pytest.fixture
def architext() -> Architext:
    uow = FakeUnitOfWork()
    architext = Architext(uow)
    architext.handle(CreateInitialData())
    rabbithole_world = WorldTemplate(
        id="rabbithole",
        name="Down The Rabbit Hole",
        description="A magical place.",
        author_id=None,
        world_encoded_json="asdasd"
    )
    outer_world = WorldTemplate(
        id="outer",
        name="Outer Wilds",
        description="Let's explore the universe!",
        author_id=None,
        world_encoded_json="asdasd"
    )
    uow.world_templates.save_world_template(rabbithole_world)
    uow.world_templates.save_world_template(outer_world)
    return Architext(uow)


def test_list_world_templates(architext: Architext):
    out = architext.query(ListWorldTemplates())
    print(out)
    assert len(out.templates) == 2
    outer = next((world for world in out.templates if world.id == "outer"), None)
    assert outer is not None
    assert outer.id == "outer"
    assert outer.description == "Let's explore the universe!"
