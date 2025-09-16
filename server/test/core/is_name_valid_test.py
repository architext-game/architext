from typing import cast
from architext.core.application.queries.is_name_valid import IsNameValid
from architext.core import Architext


def test_is_name_valid_with_good_name(architext: Architext):
    result = architext.query(IsNameValid(name="Good name", in_room_id="olivers"), client_user_id="oliver")
    assert result.is_valid == True
    assert result.error is None


def test_is_name_valid_with_duplicated_name(architext: Architext):
    result = architext.query(IsNameValid(name="To tHe sPaCeSHiP", in_room_id="olivers"), client_user_id="oliver")
    assert result.is_valid == False
    assert result.error == 'duplicated'


