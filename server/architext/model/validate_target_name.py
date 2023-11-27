import architext.entities.exceptions as exceptions
import re
import architext.entities as entities
import architext.domain.model as model

def validate_non_placed_name(
    name: str
):
    validate_target_name(name=name)

def validate_non_takable_name(
    name: str,
    others_in_room: [str],
    takables_in_world: [str],
):
    validate_target_name(
        name=name,
        is_in_a_room=True,
        is_takable=False,
        others_in_room=others_in_room,
        takables_in_world=takables_in_world
    )

def validate_takable_name(
    name: str,
    others_in_room: [str],
    takables_in_world: [str],
    all_in_world: [str]
):
    validate_target_name(
        name=name,
        is_in_a_room=True,
        is_takable=True,
        others_in_room=others_in_room,
        takables_in_world=takables_in_world,
        all_in_world=all_in_world
    )

def validate_target_name(
        name: str,
        is_in_a_room: bool = False,
        is_takable: bool = False,
        others_in_room: [str] = [],
        takables_in_world: [str] = [],
        all_in_world: [str] = []
    ):

    if len(name) == 0:
        raise exceptions.EmptyName()

    if re.search(r"#\d+$", name):
        raise exceptions.WrongNameFormat()

    if is_in_a_room and name in others_in_room:
        raise exceptions.RoomNameClash()

    if is_in_a_room and name in takables_in_world:
        raise exceptions.TakableItemNameClash()

    if is_in_a_room and is_takable and name in all_in_world:
        raise exceptions.NameNotGloballyUnique()
