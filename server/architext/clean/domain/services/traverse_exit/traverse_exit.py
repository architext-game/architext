from architext.clean.domain.unit_of_work.unit_of_work import UnitOfWork
from architext.clean.domain.events.events import UserChangedRoom
from pydantic import BaseModel, Field

class TraverseExitInput(BaseModel):
    exit_name: str

class TraverseExitOutput(BaseModel):
    new_room_id: str

def traverse_exit(uow: UnitOfWork, input: TraverseExitInput, client_user_id: str) -> TraverseExitOutput:
    with uow:
        user = uow.users.get_user_by_id(user_id=client_user_id)

        if user is None or user.room_id is None:
            raise ValueError("User is not in a room.")
    
        previous_room = uow.rooms.get_room_by_id(user.room_id)
        assert previous_room is not None
        destination_id = previous_room.get_exit_destination_id(input.exit_name)
    
        if destination_id is None:
            raise ValueError("An exit with that name was not found in the room.")

        user.room_id = destination_id

        uow.publish_events([UserChangedRoom(user_id=user.id, exit_used=input.exit_name, room_entered=destination_id, room_left=previous_room.id)])

        return TraverseExitOutput(new_room_id= user.room_id)