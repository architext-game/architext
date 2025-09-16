from typing import Callable, List
from architext.core.adapters.fake.external_event_publisher import FakeExternalEventPublisher
from architext.core.adapters.sqlalchemy.repository.rooms import SQLAlchemyRoomRepository
from architext.core.adapters.sqlalchemy.repository.users import SQLAlchemyUserRepository
from architext.core.adapters.sqlalchemy.repository.worlds import SQLAlchemyWorldRepository
from architext.core.adapters.sqlalchemy.repository.world_templates import SQLAlchemyWorldTemplateRepository
from architext.core.adapters.sqlalchemy.repository.missions import SQLAlchemyMissionRepository
from architext.core.domain.events import Event
from architext.core.application.messagebus import MessageBus
from architext.core.application.ports.notifier import Notifier
from architext.core.application.ports.unit_of_work import Transaction, UnitOfWork
from architext.core.application.queries.querymanager import QueryManager, uow_query_handlers_factory
from sqlalchemy.orm import Session, sessionmaker


class SQLAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session_factory: sessionmaker, notifier: Notifier) -> None:
        self.session_factory = session_factory
        self.db_session: Session = self.session_factory()
        self.queries = QueryManager(uow_query_handlers_factory(self))
        self._external_events = FakeExternalEventPublisher(self)
        self._notifier = notifier
        self.published_events: List[Event] = []  # to keep track of published events in tests


    def _publish_events(self, events: List[Event]) -> None:
        super()._publish_events(events)
        self.published_events += events

    def _commit(self):
        self.db_session.commit()

    def __enter__(self) -> Transaction:
        self.db_session = self.session_factory()

        return Transaction(
            external_events=self._external_events,
            notifier=self._notifier,
            missions=SQLAlchemyMissionRepository(self.db_session),
            rooms=SQLAlchemyRoomRepository(self.db_session),
            users=SQLAlchemyUserRepository(self.db_session),
            worlds=SQLAlchemyWorldRepository(self.db_session),
            world_templates=SQLAlchemyWorldTemplateRepository(self.db_session),
            _uow=self,
        )

    def rollback(self):
        self.db_session.rollback()
        self.db_session.close()
    