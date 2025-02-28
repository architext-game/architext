from typing import Callable, cast
import pytest
from architext.chatbot.adapters.chatbot_notifier import ChatbotNotifier
from architext.chatbot.adapters.fake_messaging_channel import FakeMessagingChannel
from architext.chatbot.adapters.stdout_logger import StdOutLogger
from architext.chatbot.session import Session
from architext.core.adapters.fake_notifier import FakeNotifier
from architext.core.adapters.fake_uow import FakeUnitOfWork
from architext.core.adapters.multi_notifier import MultiNotifier, multi_notifier_mapping_factory
from architext.core.adapters.sqlalchemy.session import db_connection
from architext.core.adapters.sqlalchemy.uow import SQLAlchemyUnitOfWork
from architext.core.facade import Architext
from architext.core.ports.notifier import Notifier
from architext.core.ports.unit_of_work import UnitOfWork
from test.fixtures import add_test_data

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
def notifier(channel: FakeMessagingChannel) -> Notifier:
    return MultiNotifier(multi_notifier_mapping_factory(
        chatbot=ChatbotNotifier(channel=channel),
        web=FakeNotifier()
    ))

@pytest.fixture
def uow(notifier: Notifier, request: pytest.FixtureRequest) -> UnitOfWork:
    use_db = request.config.getoption("--db")
    uow: UnitOfWork
    if use_db:
        uow = SQLAlchemyUnitOfWork(session_factory=db_connection(), notifier=notifier)
    else:
        uow = FakeUnitOfWork(notifier=notifier)
    return uow

@pytest.fixture
def architext(uow: FakeUnitOfWork):
    add_test_data(uow)
    return Architext(uow)

@pytest.fixture
def fake_notifier() -> Notifier:
    return FakeNotifier()

@pytest.fixture
def fake_notifier_uow(fake_notifier: Notifier, request: pytest.FixtureRequest) -> UnitOfWork:
    use_db = request.config.getoption("--db")
    uow: UnitOfWork
    if use_db:
        uow = SQLAlchemyUnitOfWork(session_factory=db_connection(), notifier=fake_notifier)
    else:
        uow = FakeUnitOfWork(notifier=fake_notifier)
    return uow

@pytest.fixture
def fake_notifier_architext(fake_notifier_uow: UnitOfWork) -> Architext:
    add_test_data(fake_notifier_uow)
    return Architext(fake_notifier_uow)
    

@pytest.fixture
def session_factory(architext: Architext, channel: FakeMessagingChannel) -> Callable[[str], Session]:
    def factory(user_id: str):
        return Session(architext=architext, messaging_channel=channel, logger=StdOutLogger(), user_id=user_id) 
    return factory

