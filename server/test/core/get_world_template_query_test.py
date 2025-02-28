from architext.core.queries.get_template import GetWorldTemplate
import pytest # type: ignore
from architext.core import Architext


def test_can_get_private_world_template_from_other_user(architext: Architext):
    out = architext.query(GetWorldTemplate(template_id="rabbittemplate"), client_user_id="oliver")
    assert out.id == "rabbittemplate"
    assert out.name == "Misterious Template"
    assert out.owner == "rabbit"