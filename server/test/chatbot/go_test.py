from typing import Callable
from architext.chatbot.adapters.fake_messaging_channel import FakeMessagingChannel
from architext.chatbot.session import Session
import re


def test_go(channel: FakeMessagingChannel, session_factory: Callable[[str], Session]):
    session = session_factory("oliver")
    session.process_message("go bob")

    print(channel.all_to("oliver"))

    pattern = r"""(?P<room_name>.+?)\n   # Match room name (first line)
(?P<room_description>.+?)\n\n  # Match multiline room description (greedy match)
👤\ Players\ here:\ (?P<players>.+?)\.\n  # Match players
⮕\ Exits:\ (?P<exits>.+?)\.  # Match exits
"""

    match = re.search(pattern, channel.all_to("oliver"), re.VERBOSE | re.DOTALL)

    if match:
        room_name = match.group("room_name").strip()
        room_description = match.group("room_description").strip()
        players = match.group("players").split(", ")
        exits = match.group("exits").split(", ")

        # Assertions
        assert room_name == "Bob's Room", f"Expected room name 'Bob's Room', but got '{room_name}'"
        assert room_description == "This is Bob's Room", f"Expected room description, but got '{room_description}'"
        assert set(players) == {"Dave", "Bob"}, f"Expected players ['Bob', 'Dave'], but got {players}"
        assert set(exits) == {"To Alice's Room", "To Oliver's Room", "To the spaceship"}, f"Expected exits ['To Alice's Room', 'To Oliver's Room', 'To the spaceship'], but got {exits}"
    else:
        raise ValueError("Pattern did not match the expected format")
    

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
