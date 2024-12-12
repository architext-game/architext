from architext.domain.unit_of_work.fake.fake_uow import FakeUnitOfWork
from architext.domain.services.setup.setup import setup
from architext.domain.services.create_user.create_user import create_user, CreateUserInput
from architext.domain.services.create_connected_room.create_connected_room import create_connected_room, CreateConnectedRoomInput
from architext.domain.services.traverse_exit.traverse_exit import traverse_exit, TraverseExitInput


def test_users_get_notified_if_other_enters_or_leaves_room() -> None:
    uow = FakeUnitOfWork()
    setup(uow=uow)
    user_a = create_user(uow=uow, input=CreateUserInput(
        email='test@test.com',
        name='testerA',
        password='asdasd'
    ))
    user_b = create_user(uow=uow, input=CreateUserInput(
        email='test@test.com',
        name='testerB',
        password='asdasd'
    ))
    room = create_connected_room(
        uow=uow, 
        input=CreateConnectedRoomInput(
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
        input=TraverseExitInput(
            exit_name='go'
        ),
        client_user_id=user_a.user_id
    )
    print("HE")
    print(uow.notifications.notifications)
    assert user_b.user_id in uow.notifications.notifications
    userb_notifications = uow.notifications.notifications.get(user_b.user_id, None)
    assert userb_notifications is not None
    assert len(userb_notifications) == 1
    userb_noti = userb_notifications[0]
    assert userb_noti.event == 'other_left_room'
    assert userb_noti.data.user_name == 'testerA'

