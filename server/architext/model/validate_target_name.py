import architext.entities.exceptions as exceptions
import re
import architext.entities as entities

def _validate_target_name(
    name: str, is_takable: bool, is_in_a_room: bool, local_room, ignore_item
):
    others_in_room = [item.name for item in local_room.items+local_room.exits if item != ignore_item] if local_room else []
    takables_in_world = [takable_item.name for takable_item in entities.Item.get_items_in_world_state(local_room.world_state) if takable_item != ignore_item and takable_item.visible=='takable']
    
    items_in_world = [item.name for item in entities.Item.get_items_in_world_state(local_room.world_state) if item != ignore_item]
    exits_in_world = [item.name for item in entities.Exit.get_exits_in_world_state(local_room.world_state) if item != ignore_item]
    all_in_world = items_in_world + exits_in_world

    _validate_target_name(
        name=name, is_takable=is_takable, is_in_a_room=is_in_a_room,
        others_in_room=others_in_room, takables_in_world=takables_in_world, all_in_world=all_in_world
    )

def validate_target_name(
        name: str, is_takable: bool, is_in_a_room: bool, 
        others_in_room: [str] = [], 
        takables_in_world: [str] = [], 
        all_in_world: [str] = []
    ):

    if len(name) == 0:
        raise exceptions.EmptyName()
    
    if re.search("#\d+$", name):
        raise exceptions.WrongNameFormat()
    
    if is_in_a_room and name in others_in_room:
        raise exceptions.RoomNameClash()
    
    if is_in_a_room and name in takables_in_world:
        raise exceptions.TakableItemNameClash()
    
    if is_in_a_room and is_takable and name in all_in_world:
        raise exceptions.NameNotGloballyUnique()
