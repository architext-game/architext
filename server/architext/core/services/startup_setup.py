from architext.core.commands import StartupSetup, StartupSetupResult
from architext.core.ports.unit_of_work import UnitOfWork


def startup_setup(uow: UnitOfWork, command: StartupSetup, client_user_id: str) -> StartupSetupResult:
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
                uow.users.save_user(user.with_changes(active=False))

        uow.commit()

    return StartupSetupResult()