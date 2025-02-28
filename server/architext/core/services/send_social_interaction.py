from architext.core.commands import SendSocialInteraction, SendSocialInteractionResult
from architext.core.ports.notifier import SocialInteractionNotification
from architext.core.ports.unit_of_work import UnitOfWork
from architext.core.domain.events import UserChangedRoom


def send_social_interaction(uow: UnitOfWork, command: SendSocialInteraction, client_user_id: str) -> SendSocialInteractionResult:
    with uow as transaction:
        user = transaction.users.get_user_by_id(user_id=client_user_id)

        if user is None:
            raise ValueError("User does not exist.")

        if user.room_id is None:
            raise ValueError("User is not in a room.")
    
        room = transaction.rooms.get_room_by_id(user.room_id)
        assert room is not None

        users_in_room = transaction.users.get_users_in_room(room.id)

        for other_user in users_in_room:
            transaction.notifier.notify(other_user.id, SocialInteractionNotification(
                user_name=user.name,
                content=command.content,
                kind=command.type,
            ))

        return SendSocialInteractionResult()