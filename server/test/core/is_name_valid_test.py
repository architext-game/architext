from typing import cast
from architext.core.adapters.fake_uow import FakeUnitOfWork
from architext.core.domain.entities.world import DEFAULT_WORLD
from architext.core.messagebus import MessageBus
from architext.core.queries.get_current_room import GetCurrentRoom, GetCurrentRoomResult
from architext.core.queries.is_name_valid import IsNameValid
import pytest # type: ignore
from architext.core.domain.entities.user import User
from architext.core.domain.entities.room import Room
from architext.core import Architext
from test.fixtures import createTestArchitext


@pytest.fixture
def architext() -> Architext:
    return createTestArchitext()


def test_is_name_valid_with_good_name(architext: Architext):
    result = architext.query(IsNameValid(name="Good name"), client_user_id="oliver")
    assert result.is_valid == True
    assert result.error is None


def test_is_name_valid_with_duplicated_name(architext: Architext):
    result = architext.query(IsNameValid(name="To tHe sPaCeSHiP"), client_user_id="oliver")
    assert result.is_valid == False
    assert result.error == 'duplicated'


