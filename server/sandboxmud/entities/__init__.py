import mongoengine

from .custom_verb import CustomVerb
from .item import Item
from .world import World
from .world_state import WorldState
from .world_snapshot import WorldSnapshot
from .inventory import Inventory
from .exit import Exit
from .room import Room
from .user import User

from .exceptions import BadItem, EmptyName, WrongNameFormat, RoomNameClash, TakableItemNameClash, NameNotGloballyUnique, CantDelete

# delete rules
# example:
#   Entity1.register_delete_rule(Entity2, 'reference_field', delete_rule) 
# means:
#   when a document of type Entity1 is deleted, delete_rule happens to all Entity2 that referenced that Entity1 on its field 'referencefield'
# Note: rules are only applied to database, not runtime instances. They must be reloaded.
CustomVerb.register_delete_rule(Room, 'custom_verbs', mongoengine.PULL)
CustomVerb.register_delete_rule(Item, 'custom_verbs', mongoengine.PULL)
CustomVerb.register_delete_rule(WorldState, 'custom_verbs', mongoengine.PULL)
Item.register_delete_rule(Inventory, 'items', mongoengine.PULL)
Room.register_delete_rule(User, 'room', mongoengine.NULLIFY)
Room.register_delete_rule(Item, 'room', mongoengine.CASCADE)
Room.register_delete_rule(Exit, 'room', mongoengine.CASCADE)
Room.register_delete_rule(Exit, 'destination', mongoengine.CASCADE)
WorldState.register_delete_rule(Room, 'world_state', mongoengine.CASCADE) 
WorldState.register_delete_rule(Inventory, 'world_state', mongoengine.CASCADE)
WorldSnapshot.register_delete_rule(World, 'snapshots', mongoengine.PULL)