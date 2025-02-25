from typing import Callable, List
from architext.core.adapters.fake_external_event_publisher import FakeExternalEventPublisher
from architext.core.adapters.fake_notifier import FakeNotifier
from architext.core.adapters.memory_world_repository import MemoryWorldRepository
from architext.core.adapters.memory_world_template_repository import MemoryWorldTemplateRepository
from architext.core.adapters.sqlalchemy.room_repository import SQLAlchemyRoomRepository
from architext.core.adapters.sqlalchemy.user_repository import SQLAlchemyUserRepository
from architext.core.adapters.sqlalchemy.world_repository import SQLAlchemyWorldRepository
from architext.core.adapters.sqlalchemy.world_template_repository import SQLAlchemyWorldTemplateRepository
from architext.core.adapters.sqlalchemy.mission_repository import SQLAlchemyMissionRepository
from architext.core.domain.events import Event
from architext.core.adapters.memory_room_repository import MemoryRoomRepository
from architext.core.adapters.memory_user_repository import MemoryUserRepository
from architext.core.messagebus import MessageBus
from architext.core.ports.unit_of_work import UnitOfWork
from architext.core.querymanager import QueryManager, uow_query_handlers_factory
from sqlalchemy.orm import Session, sessionmaker


class SQLAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session_factory: sessionmaker) -> None:
        self.session_factory = session_factory
        self.db_session: Session = self.session_factory()
        self.users = SQLAlchemyUserRepository(self.db_session)
        self.rooms = SQLAlchemyRoomRepository(self.db_session)
        self.worlds = SQLAlchemyWorldRepository(self.db_session)
        self.world_templates = SQLAlchemyWorldTemplateRepository(self.db_session)
        self.missions = SQLAlchemyMissionRepository(self.db_session)
        self.queries = QueryManager(uow_query_handlers_factory(self))
        self.messagebus = MessageBus()
        self.external_events = FakeExternalEventPublisher(self)
        self.notifier = FakeNotifier()
        self.published_events: List[Event] = []  # to keep track of published events in tests
        self.committed = False


    def publish_events(self, events: List[Event]) -> None:
        super().publish_events(events)
        self.published_events += events

    def _commit(self):
        self.committed = True
        self.db_session.commit()

    def __enter__(self) -> None:
        self.committed = False
        self.db_session = self.session_factory()
        self.users = SQLAlchemyUserRepository(self.db_session)
        self.rooms = SQLAlchemyRoomRepository(self.db_session)
        self.worlds = SQLAlchemyWorldRepository(self.db_session)
        self.world_templates = SQLAlchemyWorldTemplateRepository(self.db_session)
        self.missions = SQLAlchemyMissionRepository(self.db_session)

    def rollback(self):
        self.db_session.rollback()
        self.db_session.close()
        print("Session closed")
    