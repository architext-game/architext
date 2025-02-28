from architext.core.queries.get_world import GetWorld
import pytest # type: ignore
from architext.core import Architext


def test_get_world_query_success(architext: Architext):
    out = architext.query(GetWorld(world_id="outer"), client_user_id="oliver")
    assert out.id == "outer"
    assert out.name == "Outer Wilds"
    assert out.description == "Let's explore the universe!"
    assert out.connected_players_count == 2