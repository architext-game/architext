from typing import Callable
from architext.chatbot.adapters.fake_messaging_channel import FakeMessagingChannel
from architext.chatbot.session import Session


def test_exits_verb(session_factory: Callable[[str], Session]):
    session = session_factory("oliver")
    session.process_message("exits")
    assert isinstance(session.sender.channel, FakeMessagingChannel)
    sender: FakeMessagingChannel = session.sender.channel

    sent_text = '\n'.join([message.text for message in sender._sent])
    print(sent_text)
    assert "To the spaceship" in sent_text
    assert "To Alice's Room" in sent_text
    assert "To Bob's Room" in sent_text
    assert "Visible door to bathroom" in sent_text
    assert "Auto door to bathroom" in sent_text  # auto shows even when it is mentioned
    assert "Secret exit" not in sent_text
    assert "I don't understand that." not in sent_text

    # Check if verb yields control
    session.process_message("adadasdas")
    sent_text = '\n'.join([message.text for message in sender._sent])
    assert "I don't understand that." in sent_text
