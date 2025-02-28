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
            world_description="Here you will learn the basics of Architext in just five minutes. Also, this world is your exclusive property, so you can use it to give building something a try!",
            text_representation=TUTORIAL,
            format="plain",
            visibility="private",
        )])
