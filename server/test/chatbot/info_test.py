from typing import Callable
from architext.chatbot.adapters.fake_messaging_channel import FakeMessagingChannel
from architext.chatbot.session import Session


def test_info_shows_name_id_and_description(session_factory: Callable[[str], Session]):
    session = session_factory("oliver")
    session.process_message("info")
    assert isinstance(session.sender.channel, FakeMessagingChannel)
    sender: FakeMessagingChannel = session.sender.channel

    sent_text = '\n'.join([message.text for message in sender._sent])
    print(sent_text)
    assert "Oliver's Room" in sent_text
    assert "This is Oliver's Room" in sent_text
    assert "olivers" in sent_text


def test_info_shows_all_exits(session_factory: Callable[[str], Session]):
    session = session_factory("oliver")
    session.process_message("info")
    assert isinstance(session.sender.channel, FakeMessagingChannel)
    sender: FakeMessagingChannel = session.sender.channel

    sent_text = '\n'.join([message.text for message in sender._sent])
    print(sent_text)
    assert "To the spaceship" in sent_text
    assert "To Alice's Room" in sent_text
    assert "To Bob's Room" in sent_text
    assert "To Alice's Room" in sent_text
    assert "Visible door to bathroom" in sent_text
    assert "Auto door to bathroom" in sent_text
    assert "Secret exit" in sent_text

def test_info_shows_all_items(session_factory: Callable[[str], Session]):
    session = session_factory("oliver")
    session.process_message("info")
    assert isinstance(session.sender.channel, FakeMessagingChannel)
    sender: FakeMessagingChannel = session.sender.channel

    sent_text = '\n'.join([message.text for message in sender._sent])
    print(sent_text)
    assert "A cube" in sent_text
    assert "A small cube" in sent_text
    assert "A toroid" in sent_text
    assert "A sphere" in sent_text
    assert "One pyramid" in sent_text  # hidden item
