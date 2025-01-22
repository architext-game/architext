from architext.core.domain.entities.world_template import WorldTemplate
from architext.core.ports.unit_of_work import UnitOfWork
from architext.core.domain.entities.room import DEFAULT_ROOM
from architext.core.domain.entities.world import DEFAULT_WORLD
from architext.core.commands import CreateInitialData, CreateInitialDataResult


def create_initial_data(uow: UnitOfWork, command: CreateInitialData, client_user_id: str = "") -> CreateInitialDataResult:
    """This service must be called before any other"""
    with uow:
        default_world = uow.worlds.get_world_by_id(DEFAULT_WORLD.id)
        if default_world is None:
            uow.worlds.save_world(DEFAULT_WORLD)
            uow.rooms.save_room(DEFAULT_ROOM)
            default_template = WorldTemplate(
                author_id=None,
                description="Just for testing",
                id="test_template",
                name="Test Template",
                world_encoded_json="""eJx9kcFOwzAMhl/F9MKl4gG4TRxB4jCkCaFpilp3tZbEVZxOG9Penbi0tIPSS6LE9v/5ty8ZB9qTN3bnjcPsEbLXNmKADdlSshzGeIlSBGoisde0F4z3AnhqLAeEWCO0no4YBO+0jDxFSlWB2e2o1ApWYX1rXG9Jvx+XbCY69LJuTIH68Qv+zi2YhK0sm0h+D+S7Fo5GokcR4OqmpRyMZY8PKoUnij15wLxxly1Kk5qaGeKmNhEMeCoQVKFPSXCjKVOfo8x1e81hMHijPpBX8MSfZ1gvkFdQ/EmZ9/BMsajRz2p0jYtDa5OcQ4EqsFPXAResHHrFzsaE9N9e+kEWbMvvA10Tz7qRBci4+Zt5HUY3A3nJoOMSg4dJ1c+Qtkn3C67G+X8="""
            )
            uow.world_templates.save_world_template(default_template)
        uow.commit()
        
    return CreateInitialDataResult()
