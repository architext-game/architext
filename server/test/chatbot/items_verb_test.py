from typing import Callable
from architext.chatbot.adapters.fake_messaging_channel import FakeMessagingChannel
from architext.chatbot.session import Session


def test_items_verb_show_items(session_factory: Callable[[str], Session]):
    session = session_factory("oliver")
    session.process_message("items")
    assert isinstance(session.sender.channel, FakeMessagingChannel)
    sender: FakeMessagingChannel = session.sender.channel

    sent_text = '\n'.join([message.text for message in sender._sent])
    print(sent_text)
    assert "A cube" in sent_text  
    assert "A sphere" in sent_text
    assert "A small cube" in sent_text
    assert "A toroid" in sent_text


def test_item_verb_dont_show_hidden_items(session_factory: Callable[[str], Session]):
    session = session_factory("oliver")
    session.process_message("items")
    assert isinstance(session.sender.channel, FakeMessagingChannel)
    sender: FakeMessagingChannel = session.sender.channel

    sent_text = '\n'.join([message.text for message in sender._sent])
    print(sent_text)
    assert "A pyramid" not in sent_text


    
