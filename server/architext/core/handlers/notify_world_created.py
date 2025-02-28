from ast import List
from dataclasses import dataclass, asdict
from architext.core.domain.events import ShouldNotifyUserLeftRoom, ShouldNotifyWorldCreated, UserChangedRoom, WorldCreated
from architext.core.ports.unit_of_work import UnitOfWork


@dataclass
class WorldCreatedNotification:
    world_id: str
    world_name: str


def notify_world_created(uow: UnitOfWork, event: WorldCreated):
    with uow as transaction:
        world = transaction.worlds.get_world_by_id(event.world_id)
        assert world is not None

        if event.owner_id is not None:
            transaction.notifier.notify(event.owner_id, WorldCreatedNotification(
                world_id=world.id,
                world_name=world.name,
            ))
