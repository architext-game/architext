from typing import Callable
from architext.chatbot.adapters.fake_messaging_channel import FakeMessagingChannel
from architext.chatbot.session import Session


def test_go(channel: FakeMessagingChannel, session_factory: Callable[[str], Session]):
    session = session_factory("oliver")
    session.process_message("go bob")

    print(channel.all_to("oliver"))
    assert """Bob's Room
This is Bob's Room

👤 Players here: Bob, Dave.
⮕ Exits: To the spaceship, To Oliver's Room, To Alice's Room.
""" in channel.all_to("oliver")
    

def test_users_in_room_are_told_other_entered(channel: FakeMessagingChannel, session_factory: Callable[[str], Session]):
    session = session_factory("bob")
    session.process_message("go alice")
    print(channel.all_to("alice"))
    assert "Bob arrives through To Bob's Room" in channel.all_to("alice")


def test_users_in_room_are_told_other_left(channel: FakeMessagingChannel, session_factory: Callable[[str], Session]):
    session = session_factory("bob")
    session.process_message("go alice")
    print(channel.all_to("dave"))
    assert "Bob leaves through To Alice's Room." in channel.all_to("dave")
