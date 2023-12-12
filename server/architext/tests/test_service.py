import architext.service_layer.goodservices as services
from architext.adapters.repository import FakeRepository


def test_create_world():
    repo = FakeRepository()
    user_id = services.create_user(
        repository=repo,
        name="Oliver",
        password="rush2112",
        email="oliver@mail.com",
    )
    world_id = services.create_world(
        user_id=user_id,
        repository=repo,
        name='My world',
        room_description='This is the room',
        room_name='Starting room'
    )
    world = repo.get_world(world_id)
    world_state = repo.get_world_state(world.world_state_id)
    room = repo.get_room(world_state.starting_room_id)
    room = repo.get_starting_room_of_world(world.id)
    assert len(room.exit_ids) == 0
    assert len(room.item_ids) == 0
    assert room.world_state_id == world_state.id
    assert room.name == 'Starting room'


def test_create_user():
    repo = FakeRepository()
    id = services.create_user(
        repository=repo,
        name="Oliver",
        password="rush2112",
        email="oliver@mail.com",
    )
    user = repo.get_user(id)
    assert user.name == 'Oliver'
    assert user.email == 'oliver@mail.com'


def test_create_connected_room():
    repo = FakeRepository()
    world_id = services.create_world(
        user_id='USER1',
        repository=repo,
        name='My world',
        room_description='This is the room',
        room_name='Starting room'
    )

    exit_room_id = repo.get_starting_room_of_world(world_id).id

    room_id = services.create_connected_room(
        description='this is a new room',
        entrance_name='to new room',
        exit_name='to old room',
        exit_room_id=exit_room_id,
        name='new room',
        user_id='USER1',
        repository=repo
    )

    old_room_exits = repo.get_exits_in_room(exit_room_id)
    new_room = repo.get_room(room_id)
    new_room_exits = repo.get_exits_in_room(new_room.id)

    assert 'to new room' in [exit.name for exit in old_room_exits]
    assert 'to old room' in [exit.name for exit in new_room_exits]
    assert new_room.name == 'new room'

def test_create_worlde():
    repo = FakeRepository()
    user_id = services.create_user(
        repository=repo,
        name="Oliver",
        password="rush2112",
        email="oliver@mail.com",
    )
    world_id = services.create_world(
        user_id=user_id,
        repository=repo,
        name='My world',
        room_description='This is the room',
        room_name='Starting room'
    )
    world = repo.get_world(world_id)
    world_state = repo.get_world_state(world.world_state_id)
    room = repo.get_room(world_state.starting_room_id)
    room = repo.get_starting_room_of_world(world.id)
    assert len(room.exit_ids) == 0
    assert len(room.item_ids) == 0
    assert room.world_state_id == world_state.id
    assert room.name == 'Starting room'


def test_enter_world_first_time():
    repo = FakeRepository()
    user_id = services.create_user(
        repository=repo,
        name="Oliver",
        password="rush2112",
        email="oliver@mail.com",
    )
    world_id = services.create_world(
        user_id='OTHERUSER',
        repository=repo,
        name='My world',
        room_description='This is the room',
        room_name='Starting room'
    )
    world = repo.get_world(world_id)
    world_state = repo.get_world_state(world.world_state_id)
    services.enter_world(
        repository=repo,
        user_id=user_id,
        world_id=world.id
    )
    assert world_state.id == repo.get_user(user_id).current_world_state_id
    assert repo.get_avatar(user_id=user_id, world_state_id=world_state.id).current_room_id == world_state.starting_room_id

def test_use_exit():
    repo = FakeRepository()
    user_id = services.create_user(
        repository=repo,
        name="Oliver",
        password="rush2112",
        email="oliver@mail.com",
    )
    world_id = services.create_world(
        user_id=user_id,
        repository=repo,
        name='My world',
        room_description='This is the room',
        room_name='Starting room'
    )

    world = repo.get_world(world_id)
    exit_room = repo.get_starting_room_of_world(world_id)
    assert len(exit_room.exit_ids) == 0
    new_room_id = services.create_connected_room(
        description='this is a new room',
        entrance_name='to new room',
        exit_name='to old room',
        exit_room_id=exit_room.id,
        name='new room',
        user_id=user_id,
        repository=repo
    )

    services.enter_world(
        repository=repo,
        user_id=user_id,
        world_id=world.id
    )

    exit_room = repo.get_starting_room_of_world(world_id)

    services.use_exit(
        repository=repo,
        exit_name='new',
        user_id=user_id
    )

    avatar = repo.get_avatar(user_id=user_id, world_state_id=world.world_state_id)
    assert avatar.current_room_id == new_room_id

def test_look():
    repo = FakeRepository()
    user_id = services.create_user(
        repository=repo,
        name="Oliver",
        password="rush2112",
        email="oliver@mail.com",
    )
    data = services.look(repository=repo, user_id=user_id)
    print(data)
    assert data == {'room': {'name': 'First room', 'description': 'Your first room is this'}, 'exits': []}