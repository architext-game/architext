from architext.adapters.memory_uow import MemoryUnitOfWork
from architext.core.commands import TraverseExit, CreateInitialData, CreateConnectedRoom, CreateUser
from architext.core.messagebus import MessageBus
from architext.core.services.create_connected_room import create_connected_room
from architext.core.services.create_user import create_user
from architext.core.services.create_initial_data import create_initial_data
from architext.core.services.traverse_exit import traverse_exit

def test_users_get_notified_if_other_enters_or_leaves_room() -> None:
    uow = MemoryUnitOfWork()
    bus = MessageBus()
    bus.handle(uow, CreateInitialData())
    user_a = bus.handle(uow, CreateUser(
        email='test@test.com',
        name='testerA',
        password='asdasd'
    ))[0]
    user_b = bus.handle(uow, CreateUser(
        email='test@test.com',
        name='testerB',
        password='asdasd'
    ))[0]
    room = bus.handle(
        uow=uow, 
        message=CreateConnectedRoom(
            name='rrom',
            description='descripdsdas',
            exit_to_new_room_name='go',
            exit_to_new_room_description='hehe',
            exit_to_old_room_name='return',
            exit_to_old_room_description='hoho'
        ),
        client_user_id=user_a.user_id
    )[0]
    bus.handle(
        uow=uow,
        message=TraverseExit(
            exit_name='go'
        ),
        client_user_id=user_a.user_id
    )
    assert user_b.user_id in uow.notifications.notifications
    userb_notifications = uow.notifications.notifications.get(user_b.user_id, None)
    assert userb_notifications is not None
    assert len(userb_notifications) == 1
    userb_noti = userb_notifications[0]
    assert userb_noti.event == 'other_left_room'
    assert userb_noti.data.user_name == 'testerA'

