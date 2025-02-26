from architext.content.the_monks_riddle import THE_MONKS_RIDDLE_ENCODED
from architext.core.commands import Setup, SetupResult
from architext.core.domain.entities.mission import default_missions
from architext.core.domain.entities.world_template import WorldTemplate
from architext.core.domain.events import WorldCreationRequested
from architext.core.ports.unit_of_work import UnitOfWork


def setup(uow: UnitOfWork, command: Setup, client_user_id: str) -> SetupResult:
    """Should be run each time the server is restarted, 
    assuming we have no more than a single server instance
    at any given time"""
    with uow:
        # When server stopped some users may remain as active.
        # We should set them as inactive.
        # TODO: This is because we have persistence where we don't want it.
        # We should store active status in a different non persistent
        # repository, separate from the user entity.
        users = uow.users.list_users()
        for user in users:
            if user.active:
                user.active=False
                uow.users.save_user(user)

        if should_insert_initial_data(uow):
            print("STARTUP: Adding initial data")
            uow.external_events.publish(WorldCreationRequested(
                future_world_id='monks_riddle',
                user_id=None,
                world_name="The Monk's Riddle",
                world_description="An abandonded monastery where a mystery waits to be unraveled. Good to play with friends or alone in about 30 minutes.",
                text_representation=THE_MONKS_RIDDLE_ENCODED,
                format='encoded',
                visibility='public',
            ))
            emptytemplate = WorldTemplate(
                id="empty_template",
                name="New World",
                description="Create an empty world for you to build on.",
                author_id=None,
                world_encoded_json="""eJx9kcFOwzAMhl/F9MKl4gG4TRxB4jCkCaFpilp3tZbEVZxOG9Penbi0tIPSS6LE9v/5ty8ZB9qTN3bnjcPsEbLXNmKADdlSshzGeIlSBGoisde0F4z3AnhqLAeEWCO0no4YBO+0jDxFSlWB2e2o1ApWYX1rXG9Jvx+XbCY69LJuTIH68Qv+zi2YhK0sm0h+D+S7Fo5GokcR4OqmpRyMZY8PKoUnij15wLxxly1Kk5qaGeKmNhEMeCoQVKFPSXCjKVOfo8x1e81hMHijPpBX8MSfZ1gvkFdQ/EmZ9/BMsajRz2p0jYtDa5OcQ4EqsFPXAResHHrFzsaE9N9e+kEWbMvvA10Tz7qRBci4+Zt5HUY3A3nJoOMSg4dJ1c+Qtkn3C67G+X8=""",
                visibility="public"
            )
            uow.world_templates.save_world_template(emptytemplate)
            for mission in default_missions().all:
                uow.missions.save_mission(mission)
            uow.commit()
        else:
            print("STARTUP: Initial data found")
            uow.commit()

    return SetupResult()

def should_insert_initial_data(uow: UnitOfWork) -> bool:
    return len(uow.world_templates.list_world_templates()) == 0