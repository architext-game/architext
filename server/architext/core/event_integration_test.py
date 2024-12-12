from architext.adapters.memory_uow import MemoryUnitOfWork
from architext.core.commands import TraverseExit, CreateInitialData, CreateConnectedRoom, CreateUser
from architext.core.services.create_connected_room import create_connected_room
from architext.core.services.create_user import create_user
from architext.core.services.create_initial_data import create_initial_data
from architext.core.services.traverse_exit import traverse_exit

def test_users_get_notified_if_other_enters_or_leaves_room() -> None:
    uow = MemoryUnitOfWork()
    create_initial_data(uow=uow, command=CreateInitialData())
    user_a = create_user(uow=uow, command=CreateUser(
        email='test@test.com',
        name='testerA',
        password='asdasd'
    ))
    user_b = create_user(uow=uow, command=CreateUser(
        email='test@test.com',
        name='testerB',
        password='asdasd'
    ))
    room = create_connected_room(
        uow=uow, 
        command=CreateConnectedRoom(
            name='rrom',
            description='descripdsdas',
            exit_to_new_room_name='go',
            exit_to_new_room_description='hehe',
            exit_to_old_room_name='return',
            exit_to_old_room_description='hoho'
        ),
        client_user_id=user_a.user_id
    )
    traverse_exit(
        uow=uow,
        command=TraverseExit(
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

