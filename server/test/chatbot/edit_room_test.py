from csv import Error
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


def test_edit_room_name_success(session_factory: Callable[[str], Session]):
    try:
        session = session_factory("oliver")
        assert isinstance(session.sender, FakeSender)
        sender: FakeSender = session.sender
        
        session.process_message("edit")
        assert "Editing room Oliver's Room" in sender.unread
        session.process_message("1")
        assert "Enter the new name:" in sender.unread
        session.process_message("MY COOL ROOM!")
        assert "Edition completed" in sender.unread
        session.process_message("asdasd")
        assert "I don't understand that." in sender.unread

        uow = session.architext._uow
        olivers = uow.rooms.get_room_by_id("olivers")
        assert olivers is not None
        assert olivers.name == "MY COOL ROOM!"
    except:
        print(sender.all)
        raise
    

def test_edit_room_description_success(session_factory: Callable[[str], Session]):
    try:
        session = session_factory("oliver")
        assert isinstance(session.sender, FakeSender)
        sender: FakeSender = session.sender
        
        session.process_message("edit")
        assert "Editing room" in sender.unread
        session.process_message("2")
        assert "description" in sender.unread
        session.process_message("There is a poster that reads \"2112\"")
        assert "Edition completed" in sender.unread
        session.process_message("asdasd")
        assert "I don't understand that." in sender.unread

        uow = session.architext._uow
        olivers = uow.rooms.get_room_by_id("olivers")
        assert olivers is not None
        assert olivers.description == "There is a poster that reads \"2112\""
    except:
        print(sender.all)
        raise
