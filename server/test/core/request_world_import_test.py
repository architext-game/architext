from typing import cast
from architext.core.adapters.fake_external_event_publisher import FakeExternalEventPublisher
from architext.core.adapters.fake_uow import FakeUnitOfWork
from architext.core.commands import RequestWorldImport
import pytest # type: ignore
from architext.core.domain.entities.user import User
from architext.core.domain.events import WorldCreationRequested
from architext.core import Architext


ENCODED_TEMPLATE = """eJx9kcFOwzAMhl/F9MKl4gG4TRxB4jCkCaFpilp3tZbEVZxOG9Penbi0tIPSS6LE9v/5ty8ZB9qTN3bnjcPsEbLXNmKADdlSshzGeIlSBGoisde0F4z3AnhqLAeEWCO0no4YBO+0jDxFSlWB2e2o1ApWYX1rXG9Jvx+XbCY69LJuTIH68Qv+zi2YhK0sm0h+D+S7Fo5GokcR4OqmpRyMZY8PKoUnij15wLxxly1Kk5qaGeKmNhEMeCoQVKFPSXCjKVOfo8x1e81hMHijPpBX8MSfZ1gvkFdQ/EmZ9/BMsajRz2p0jYtDa5OcQ4EqsFPXAResHHrFzsaE9N9e+kEWbMvvA10Tz7qRBci4+Zt5HUY3A3nJoOMSg4dJ1c+Qtkn3C67G+X8="""

def test_request_world_import_success(architext: Architext):
    out = architext.handle(RequestWorldImport(
        name="new world",
        description="nice",
        text_representation=ENCODED_TEMPLATE,
        format='encoded'
    ), client_user_id="oliver")

    with architext._uow as transaction:
        external_events = cast(FakeExternalEventPublisher, transaction.external_events)
        creation_request_event = next((event for event in external_events.published_events if type(event) == WorldCreationRequested), None)
        assert creation_request_event is not None
        assert creation_request_event.format == 'encoded'
        assert creation_request_event.user_id == "oliver"
        assert creation_request_event.text_representation == ENCODED_TEMPLATE
