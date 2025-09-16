from typing import Callable
from architext.chatbot import strings
from architext.chatbot.adapters.fake_messaging_channel import FakeMessagingChannel
from architext.chatbot.session import Session
from architext.core.application.settings import EXIT_NAME_MAX_LENGTH, ROOM_DESCRIPTION_MAX_LENGTH, ROOM_NAME_MAX_LENGTH


def test_build_success(channel: FakeMessagingChannel, session_factory: Callable[[str], Session]):
    session = session_factory("oliver")

    session.process_message("build")
    session.process_message("Living Room")
    session.process_message("A cozy living room")
    session.process_message("Door to living room")
    session.process_message("Door to kitchen")
    session.process_message("adadasdas")

    sent_text = channel.all_to("oliver")
    print(sent_text)

    uow = session.architext._uow
    with uow as transaction:
        new_room = next((room for room in transaction.rooms.list_rooms() if room.name == "Living Room"), None)
        old_room = transaction.rooms.get_room_by_id("olivers")
        assert new_room is not None
        assert old_room is not None
        assert new_room.name == "Living Room"
        assert new_room.description == "A cozy living room"
        assert new_room.exits["Door to kitchen"].destination_room_id == old_room.id
        assert old_room.exits["Door to living room"].destination_room_id == new_room.id
        assert "I don't understand that." in sent_text  # check if "adadasdas" was processed as a new command


def test_build_error_messages(channel: FakeMessagingChannel, session_factory: Callable[[str], Session]):
    session = session_factory("oliver")

    session.process_message("build")
    # Empty room name
    session.process_message("")
    assert strings.is_empty in channel.unread
    # Long room name
    session.process_message("A"*(ROOM_NAME_MAX_LENGTH+1))
    assert "Can't be longer than" in channel.unread
    session.process_message("A proper name")

    # Long room description
    session.process_message("A"*(ROOM_DESCRIPTION_MAX_LENGTH+1))
    assert "Can't be longer than" in channel.unread
    session.process_message("A proper description")

    # Name taken by exit in room, but case does not match
    session.process_message("tO tHe sPaCeShIp")
    assert strings.room_name_clash in channel.unread
    # Long exit 1 name
    session.process_message("A"*(EXIT_NAME_MAX_LENGTH+1))
    assert "Can't be longer than" in channel.unread
    session.process_message("A proper name")
    
    # Long exit 2 name
    session.process_message("A"*(EXIT_NAME_MAX_LENGTH+1))

    assert "Can't be longer than" in channel.unread
    session.process_message("A proper name")
    assert "Your new room is ready" in channel.unread


def test_build_by_unauthorized_user(session_factory: Callable[[str], Session]):
    session = session_factory("alice")

    session.process_message("build")
    session.process_message("afafdadsdfa")
    assert isinstance(session.sender.channel, FakeMessagingChannel)
    sender: FakeMessagingChannel = session.sender.channel

    sent_text = '\n'.join([message.text for message in sender._sent])
    print(sent_text)
    assert "You don't have enough privileges to do that here." in sent_text
    assert "I don't understand that." in sent_text


def test_build_by_user_that_is_not_in_a_room(session_factory: Callable[[str], Session]):
    session = session_factory("charlie")

    session.process_message("build")
    session.process_message("afafdadsdfa")
    assert isinstance(session.sender.channel, FakeMessagingChannel)
    sender: FakeMessagingChannel = session.sender.channel

    sent_text = '\n'.join([message.text for message in sender._sent])
    print(sent_text)
    assert "You don't have enough privileges to do that here." in sent_text
    assert "I don't understand that." in sent_text