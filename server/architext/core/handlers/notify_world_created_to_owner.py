from dataclasses import dataclass, asdict
from architext.core.ports.unit_of_work import UnitOfWork
from architext.core.domain.events import WorldCreated
from typing import List

@dataclass
class WorldCreatedNotification:
    world_id: str

def notify_world_created_to_owner(uow: UnitOfWork, event: WorldCreated):
    uow.notifications.notify_user(
        event.owner_id,
        'world_created',
        asdict(WorldCreatedNotification(world_id=event.world_id))
    )