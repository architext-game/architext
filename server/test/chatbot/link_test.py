from typing import Callable
from architext.chatbot.adapters.fake_sender import FakeSender
from architext.chatbot.adapters.stdout_logger import StdOutLogger
from architext.chatbot.session import Session
import pytest # type: ignore
from test.fixtures import createTestData


@pytest.fixture
def session_factory() -> Callable[[str], Session]:
    def factory(user_id: str):
        architext = createTestData()
        return Session(architext=architext, sender=FakeSender(architext), logger=StdOutLogger(), user_id=user_id) 
    return factory


def test_link_success(session_factory: Callable[[str], Session]):
    session = session_factory("oliver")

    session.process_message("link")
    session.process_message("alices")
    session.process_message("The new exit to alices")
    session.process_message("The new exit to olivers")

    assert isinstance(session.sender, FakeSender)
    sender: FakeSender = session.sender
    sent_text = '\n'.join([message.text for message in sender._sent])
    print(sent_text)

    assert "Your new exits are ready!" in sent_text
    uow = session.architext._uow
    olivers = uow.rooms.get_room_by_id("olivers")
    assert olivers is not None
    alices = uow.rooms.get_room_by_id("alices")
    assert alices is not None
    assert next(exit for exit in olivers.exits if exit.name == "The new exit to alices") is not None
    assert next(exit for exit in olivers.exits if exit.name == "The new exit to olivers") is not None


@pytest.mark.skip(reason="Not implemented yet")
def test_link_with_room_in_other_world_fails(session_factory: Callable[[str], Session]):
    session = session_factory("oliver")

    session.process_message("link")

    assert isinstance(session.sender, FakeSender)
    sender: FakeSender = session.sender
    sent_text = '\n'.join([message.text for message in sender._sent])
    print(sent_text)

    uow = session.architext._uow
    assert False


@pytest.mark.skip(reason="Not implemented yet")
def test_link_by_unauthorized_user_fails(session_factory: Callable[[str], Session]):
    session = session_factory("oliver")

    session.process_message("link")

    assert isinstance(session.sender, FakeSender)
    sender: FakeSender = session.sender
    sent_text = '\n'.join([message.text for message in sender._sent])
    print(sent_text)

    uow = session.architext._uow
    assert False


@pytest.mark.skip(reason="Not implemented yet")
def test_link_rejects_duplicated_exits(session_factory: Callable[[str], Session]):
    session = session_factory("oliver")

    session.process_message("link")

    assert isinstance(session.sender, FakeSender)
    sender: FakeSender = session.sender
    sent_text = '\n'.join([message.text for message in sender._sent])
    print(sent_text)

    uow = session.architext._uow
    assert False