from architext.core.commands import CreateTemplate
from architext.core.queries.world_to_text import WorldToText
import pytest # type: ignore
from architext.core import Architext


def test_create_template_success(architext: Architext):
    create_template_result = architext.handle(CreateTemplate(
        name="My new template",
        description="I just made this template",
        base_world_id="outer"
    ), client_user_id="oliver")
    with architext._uow as transaction:
        template = transaction.world_templates.get_world_template_by_id(create_template_result.template_id)
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


    
    