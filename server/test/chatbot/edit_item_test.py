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


def test_edit_item_name_success(session_factory: Callable[[str], Session]):
    session = session_factory("oliver")

    session.process_message("edit toroid")
    session.process_message("1")
    session.process_message("A Donut")
    session.process_message("asdasd")

    assert isinstance(session.sender, FakeSender)
    sender: FakeSender = session.sender
    sent_text = '\n'.join([message.text for message in sender._sent])
    print(sent_text)

    assert "Edition completed" in sent_text
    assert "I don't understand that." in sent_text
    uow = session.architext._uow
    olivers = uow.rooms.get_room_by_id("olivers")
    assert olivers is not None
    assert olivers.items.get("A Donut") is not None
    assert olivers.items.get("A Toroid") is None
    

def test_edit_item_description_success(session_factory: Callable[[str], Session]):
    session = session_factory("oliver")

    session.process_message("edit Toroid")
    session.process_message("2")
    session.process_message("It's just like a donut")
    session.process_message("asdasd")
    
    assert isinstance(session.sender, FakeSender)
    sender: FakeSender = session.sender
    sent_text = '\n'.join([message.text for message in sender._sent])
    print(sent_text)

    assert "Edition completed" in sent_text
    assert "I don't understand that." in sent_text
    uow = session.architext._uow
    olivers = uow.rooms.get_room_by_id("olivers")
    assert olivers is not None
    item = olivers.items.get("A toroid")
    assert item is not None
    assert item.description == "It's just like a donut"


def test_edit_item_visibility_success(session_factory: Callable[[str], Session]):
    session = session_factory("oliver")

    session.process_message("edit A Toroid")
    session.process_message("3")
    session.process_message("Hidden")
    session.process_message("asdasd")
    
    assert isinstance(session.sender, FakeSender)
    sender: FakeSender = session.sender
    sent_text = '\n'.join([message.text for message in sender._sent])
    print(sent_text)

    assert "Edition completed" in sent_text
    assert "I don't understand that." in sent_text
    uow = session.architext._uow
    olivers = uow.rooms.get_room_by_id("olivers")
    assert olivers is not None
    item = olivers.items.get("A toroid")
    assert item is not None
    assert item.visibility == "hidden"
