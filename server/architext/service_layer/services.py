from typing import Optional, Literal
import architext.entities as entities
from architext.model.validate_target_name import validate_target_name
import architext.domain.exceptions as exceptions
import architext.util as util

def create_custom_verb(
        names: [str], commands: [str], session,
        world_state_id: Optional[str] = None,
        room_id: Optional[str] = None,
        item_id: Optional[str] = None
    ):
    new_verb = entities.CustomVerb(names=names, commands=commands)

    if world_state_id is not None:
        world_state = entities.WorldState.objects.get(id=world_state_id)
        if not world_state.get_world().is_privileged(session.user):
            raise entities.exceptions.InsufficientPrivileges()
        world_state.add_custom_verb(new_verb)

    if room_id is not None:
        room = entities.Room.objects.get(id=room_id)
        world = room.world_state.get_world()
        if not world.is_privileged(session.user):
            raise entities.exceptions.InsufficientPrivileges()
        room.add_custom_verb(new_verb)

    if item_id is not None:
        item = entities.Item.objects.get(id=item_id)
        world = item.room.world_state.get_world()
        if not world.is_privileged(session.user):
            raise entities.exceptions.InsufficientPrivileges()
        item.add_custom_verb(new_verb)


def create_connected_room(name: str, description: str, exit_name: str, entrance_name: str, exit_room_id: str, session):
    # TODO: if one creation fails, roll back
    exit_room = entities.Room.objects.get(id=exit_room_id)

    if not exit_room.world_state.get_world().is_privileged(session.user):
        raise entities.exceptions.InsufficientPrivileges()

    new_room = entities.Room(world_state=exit_room.world_state, name=name, description=description)
    create_exit(name=exit_name, location_room_id=new_room.id, destination_room_id=exit_room_id, session=session)
    create_exit(name=entrance_name, location_room_id=exit_room_id, destination_room_id=new_room.id, session=session)

def connect_rooms(room_A_id: str, room_B_id: str, session, exit_A_name: str = None, exit_B_name: str = None):
    # TODO: if one creation fails, roll back
    if not entities.Room.objects.get(id=room_A_id).world_state.get_world().is_privileged(session.user):
        raise entities.exceptions.InsufficientPrivileges()

    create_exit(location_room_id=room_A_id, destination_room_id=room_B_id, name=exit_A_name, session=session)
    create_exit(location_room_id=room_B_id, destination_room_id=room_A_id, name=exit_B_name, session=session)

def create_exit(location_room_id: str, destination_room_id: str, session, description: str = None, name: str = None):
    location = entities.Room.objects.get(id=location_room_id)

    if not location.world_state.get_world().is_privileged(session.user):
        raise entities.exceptions.InsufficientPrivileges()

    destination = entities.Room.objects.get(id=destination_room_id)
    validate_target_name(
        name=name, is_takable=False, is_in_a_room=True,
        others_in_room=[item.name for item in session.user.room.items + session.user.room.exits],
        takables_in_world=[item.name for item in entities.Item.get_items_in_world_state(session.user.room.world_state) if item.visible=='takable']
    )
    entities.Exit(destination=destination, room=location, name=name, description=description)


def create_item(
        session, name: str, description: str,
        visibility: Literal['obvious', 'listed', 'hidden', 'takable'],
        room_id: Optional[str],
        world_state_id: Optional[str]
    ):
    assert room_id or world_state_id

    world_state = entities.WorldState.objects.get(id=world_state_id) if world_state_id else None
    room = entities.Room.objects.get(id=room_id) if room_id else None

    if world_state and not world_state.get_world().is_privileged(session.user):
        raise entities.exceptions.InsufficientPrivileges()

    if room and not room.world_state.get_world().is_privileged(session.user):
        raise entities.exceptions.InsufficientPrivileges()

    validate_target_name(
        name=name,
        is_takable=visibility=='takable',
        is_in_a_room=room_id is not None,
        others_in_room=[item.name for item in session.user.room.items + session.user.room.exits],
        takables_in_world=[item.name for item in entities.Item.get_items_in_world_state(session.user.room.world_state) if item.visible=='takable'],
        all_in_world=[item.name for item in entities.Item.get_items_in_world_state(session.user.room.world_state)] + [item.name for item in entities.Exit.get_exits_in_world_state(session.user.room.world_state)]
    )

    new_item = entities.Item(
        visible=visibility,
        name=name,
        description=description,
        saved_in=world_state,
        room=room
    )

    if world_state_id:
        new_item.item_id = new_item._generate_item_id()
    if room_id:
        new_item.put_in_room(new_item.room)


def delete_room(session, room_id: str):
    room_to_delete = entities.Room.objects.get(id=room_id)

    if not room_to_delete.world_state.get_world().is_privileged(session.user):
        raise entities.exceptions.InsufficientPrivileges()
    if len([user for user in entities.User.objects(room=room_to_delete) if user.client_id != None]) > 1:
        raise exceptions.CantDeleteRoomWithPlayers()
    if room_to_delete.alias == "0":
        raise exceptions.CantDeleteStartingRoom()
    else:
        # exits connecting to this room are implicitly removed from db and from exit 
        # lists in all rooms, due to its definition in entities.py
        for item in room_to_delete.items:
            item.delete()

        for exit in room_to_delete.exits:
            exit.delete()

        room_to_escape_from_oblivion = session.user.room.world_state.starting_room
        session.user.teleport(room_to_escape_from_oblivion)
        for user in entities.User.objects(room=room_to_delete):
            user.teleport(room_to_escape_from_oblivion)

        room_to_delete.delete()


def delete_exit(session, exit_id: str):
    exit = entities.Exit.objects.get(id=exit_id)
    world = exit.room.world_state.get_world()

    if not world.is_privileged(session.user):
        raise entities.exceptions.InsufficientPrivileges()

    exit.delete()


def delete_item(session, item_id: str):
    item = entities.Item.objects.get(id=item_id)

    if not item.room.world_state.get_world().is_privileged(session.user):
        raise entities.exceptions.InsufficientPrivileges()

    item.delete()

def update_item(
        session,
        item_id: str,
        name: str = None,
        description: str = None,
        visibility: Optional[Literal['obvious', 'listed', 'hidden', 'takable']] = None
    ):

    item = entities.Item.objects.get(id=item_id)

    if item.room and not item.room.world_state.get_world().is_privileged(session.user):
        raise entities.exceptions.InsufficientPrivileges()
    if item.saved_in and not item.saved_in.get_world().is_privileged(session.user):
        raise entities.exceptions.InsufficientPrivileges()

    if name or visibility:
        validate_target_name(
            name=name if name else item.name,
            is_takable=(visibility if visibility else item.visible)=='takable', 
            is_in_a_room=item.room is not None,
            others_in_room=[item.name for item in session.user.room.items + session.user.room.exits],
            takables_in_world=[item.name for item in entities.Item.get_items_in_world_state(session.user.room.world_state) if item.visible=='takable'],
            all_in_world=[item.name for item in entities.Item.get_items_in_world_state(session.user.room.world_state)] + [item.name for item in entities.Exit.get_exits_in_world_state(session.user.room.world_state)]
        )

    if name:
        item.name = name
    if description:
        item.description = description
    if visibility:
        item.visibility = visibility

    item.save()


def update_exit(
        session,
        item_id: str,
        name: str = None,
        description: str = None,
        visibility: Optional[Literal['obvious', 'listed', 'hidden', 'takable']] = None,
        destination_room_id: Optional[str] = None
    ):

    exit = entities.Exit.objects.get(id=item_id)

    if exit.room and not exit.room.world_state.get_world().is_privileged(session.user):
        raise entities.exceptions.InsufficientPrivileges()

    if name or visibility:
        validate_target_name(
            name=name if name else exit.name,
            is_takable=False,
            is_in_a_room=True,
            others_in_room=[target.name for target in session.user.room.items + session.user.room.exits],
            takables_in_world=[item.name for item in entities.Item.get_items_in_world_state(session.user.room.world_state) if item.visible=='takable'],
            all_in_world=[item.name for item in entities.Item.get_items_in_world_state(session.user.room.world_state)] + [exit.name for exit in entities.Exit.get_exits_in_world_state(session.user.room.world_state)]
        )

    if name:
        exit.name = name
    if description:
        exit.description = description
    if visibility:
        exit.visibility = visibility
    if destination_room_id:
        exit.destination = entities.Room.objects.get(id=destination_room_id)

    exit.save()


def edit_world(
    session,
    world_id: str,
    name: Optional[str] = None,
    public: Optional[bool] = None,
    all_can_edit: Optional[bool] = None
):
    world = entities.World.objects.get(id=world_id)

    if not world.is_privileged(session.user):
        raise entities.exceptions.InsufficientPrivileges()

    if name:
        world.name = name
    if public and world.public != public:
        world.toggle_public()
    if all_can_edit == True:
        world.set_to_free_edition()
    if all_can_edit == False:
        world.set_to_privileged_edition()

    world.save()


def use_exit(session, exit_id: str):
    exit = entities.Exit.objects.get(id=exit_id)

    if not exit.room == session.user.room:
        raise exceptions.CantUseExitInAnotherRoom()

    if not session.user.master_mode:
        if not exit.is_open:
            raise exceptions.CantUseClosedExit()

    session.user.move(exit.name)


def new_world_from_json(session, name: str, json: str):
    world_dict = util.text_to_world_dict(json)
    world = util.world_from_dict(world_dict, name, session.user)
    return world  # caution


def create_world(
        session,
        name: str,
        room_name: str,
        room_description: str,
    ):
    starting_room = entities.Room(
        name=room_name,
        alias='0',
        description=room_description
    )
    world_state = entities.WorldState(starting_room=starting_room)
    return entities.World(name=name, creator=session.user, world_state=world_state)