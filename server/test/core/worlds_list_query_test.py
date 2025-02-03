from architext.core.queries.list_worlds import ListWorlds
import pytest # type: ignore
from architext.core import Architext

from test.fixtures import createTestData


@pytest.fixture
def architext() -> Architext:
    return createTestData()

def test_list_worlds(architext: Architext):
    out = architext.query(ListWorlds(), client_user_id="oliver")
    print(out)
    assert len(out.worlds) == 4
    # A public world I don't own should be on the list
    assert next((world for world in out.worlds if world.id == "tabern"), None) is not None
    # A private world I own should be on the list
    assert next((world for world in out.worlds if world.id == "oliver_place"), None) is not None
    # A private world I don't own should not be on the list
    assert next((world for world in out.worlds if world.id == "rabbithole"), None) is None
    # A private world I don't know but I've visited should be on the list
    assert next((world for world in out.worlds if world.id == "easteregg"), None) is not None
    # A public world I own should be on the list
    outer = next((world for world in out.worlds if world.id == "outer"), None)
    # A public world I own should be on the list
    assert outer is not None
    assert outer.id == "outer"
    assert outer.description == "Let's explore the universe!"
    assert outer.owner_name == "Oliver"
    assert outer.connected_players_count == 4
    assert outer.base_template_name == None
    assert outer.base_template_author == None
