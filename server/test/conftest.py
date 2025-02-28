from typing import Callable, cast
import pytest
from architext.chatbot.adapters.chatbot_notifier import ChatbotNotifier
from architext.chatbot.adapters.fake_messaging_channel import FakeMessagingChannel
from architext.chatbot.adapters.stdout_logger import StdOutLogger
from architext.chatbot.session import Session
from architext.core.adapters.fake_notifier import FakeNotifier
from architext.core.adapters.fake_uow import FakeUnitOfWork
from architext.core.adapters.multi_notifier import MultiNotifier, multi_notifier_mapping_factory
from architext.core.adapters.sqlalchemy.uow import SQLAlchemyUnitOfWork
from architext.core.facade import Architext
from architext.core.ports.unit_of_work import UnitOfWork
from test.fixtures import createTestUow

import pytest

def pytest_addoption(parser):
    """Add a custom command-line option `--db` for pytest."""
    parser.addoption(
        "--db", action="store_true", default=False, help="Use a database file instead of in-memory storage"
    )


@pytest.fixture
def channel() -> FakeMessagingChannel:
    return FakeMessagingChannel()

@pytest.fixture
def uow(channel: FakeMessagingChannel, request: pytest.FixtureRequest) -> UnitOfWork:
    use_db = request.config.getoption("--db")
    uow = createTestUow(db=use_db)
    uow._notifier = MultiNotifier(multi_notifier_mapping_factory(
        chatbot=ChatbotNotifier(channel=channel),
        web=FakeNotifier()
    ))
    return uow

@pytest.fixture
def architext(uow: FakeUnitOfWork):
    return Architext(uow)

@pytest.fixture
def session_factory(architext: Architext, channel: FakeMessagingChannel) -> Callable[[str], Session]:
    def factory(user_id: str):
        return Session(architext=architext, messaging_channel=channel, logger=StdOutLogger(), user_id=user_id) 
    return factory

@pytest.fixture
def notifier(architext: Architext) -> FakeNotifier:
    return cast(FakeNotifier, architext._uow._notifier)
