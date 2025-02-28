from architext.content.empty_world import EMPTY_WORLD, EMPTY_WORLD_ENCODED
from architext.content.the_monks_riddle import THE_MONKS_RIDDLE_ENCODED
from architext.core.commands import Setup, SetupResult
from architext.core.domain.entities.mission import default_missions
from architext.core.domain.entities.world_template import WorldTemplate
from architext.core.domain.events import WorldCreationRequested
from architext.core.ports.unit_of_work import Transaction, UnitOfWork


def setup(uow: UnitOfWork, command: Setup, client_user_id: str) -> SetupResult:
    """Should be run each time the server is restarted, 
    assuming we have no more than a single server instance
    at any given time"""
    with uow as transaction:
        # When server stopped some users may remain as active.
        # We should set them as inactive.
        # TODO: This is because we have persistence where we don't want it.
        # We should store active status in a different non persistent
        # repository, separate from the user entity.
        users = transaction.users.list_users()
        for user in users:
            if user.active:
                user.active=False
                transaction.users.save_user(user)

        if should_insert_initial_data(transaction):
            print("STARTUP: Adding initial data")
            transaction.external_events.publish(WorldCreationRequested(
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
                world_encoded_json=EMPTY_WORLD_ENCODED,
                visibility="public"
            )
            transaction.world_templates.save_world_template(emptytemplate)
            for mission in default_missions().all:
                transaction.missions.save_mission(mission)
            transaction.commit()
        else:
            print("STARTUP: Initial data found")
            transaction.commit()

    return SetupResult()

def should_insert_initial_data(transaction: Transaction) -> bool:
    return len(transaction.world_templates.list_world_templates()) == 0