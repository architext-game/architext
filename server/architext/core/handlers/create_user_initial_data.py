import uuid
from architext.content.tutorial import TUTORIAL
from architext.core.ports.unit_of_work import UnitOfWork
from architext.core.domain.events import UserCreated, WorldCreationRequested

def create_user_initial_data(uow: UnitOfWork, event: UserCreated):
    with uow as transaction:
        uow.publish_events([WorldCreationRequested(
            future_world_id=str(uuid.uuid4()),
            user_id=event.user_id,
            world_name="Tutorial World",
            world_description="In Architext you can create and explore typing a simple set of text commands. Press Enter Now to learn everything you need to know!",
            text_representation=TUTORIAL,
            format="plain",
            visibility="private",
        )])
