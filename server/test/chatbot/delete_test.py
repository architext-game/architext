from typing import Callable
from architext.chatbot.adapters.fake_sender import FakeSender
from architext.chatbot.adapters.stdout_logger import StdOutLogger
from architext.chatbot.session import Session
import pytest # type: ignore
from test.fixtures import createTestArchitext


@pytest.fixture
def session_factory() -> Callable[[str], Session]:
    def factory(user_id: str):
        architext = createTestArchitext()
        return Session(architext=architext, sender=FakeSender(architext), logger=StdOutLogger(), user_id=user_id) 
    return factory


def test_delete_item_success(session_factory: Callable[[str], Session]):
    session = session_factory("oliver")

    session.process_message("delete A toroid")
    session.process_message("asdasd")

    assert isinstance(session.sender, FakeSender)
    sender: FakeSender = session.sender
    sent_text = '\n'.join([message.text for message in sender._sent])
    print(sent_text)

    assert 'Item "A toroid" has been deleted' in sent_text
    assert "I don't understand that." in sent_text

    uow = session.architext._uow
    olivers = uow.rooms.get_room_by_id("olivers")
    assert olivers is not None
    assert olivers.items.get("A toroid") is None


def test_delete_exit_success(session_factory: Callable[[str], Session]):
    session = session_factory("oliver")

    session.process_message("delete To the spaceship")
    session.process_message("asdasd")

    assert isinstance(session.sender, FakeSender)
    sender: FakeSender = session.sender
    sent_text = '\n'.join([message.text for message in sender._sent])
    print(sent_text)

    assert 'Exit "To the spaceship" has been deleted' in sent_text
    assert "I don't understand that." in sent_text

    uow = session.architext._uow
    olivers = uow.rooms.get_room_by_id("olivers")
    assert olivers is not None
    assert olivers.exits.get("To the spaceship") is None


@pytest.mark.skip(reason="TODO")
def test_unauthorized_user_cannot_delete(session_factory: Callable[[str], Session]):
    pass


@pytest.mark.skip(reason="TODO")
def test_non_exact_name_for_delete_fails(session_factory: Callable[[str], Session]):
    pass
