import mongoengine
from . import inventory as inventory_module
from . import item as item_module
from . import room as room_module
from . import world as world_module

class WorldState(mongoengine.Document):
    starting_room = mongoengine.ReferenceField('Room', required=True)
    custom_verbs = mongoengine.ListField(mongoengine.ReferenceField('CustomVerb'))
    _next_room_id = mongoengine.IntField(default=1)

    def __init__(self, *args, save_on_creation=True, **kwargs):
        super().__init__(*args, **kwargs)

        if self.id is None:
            if save_on_creation:
                if self.starting_room.alias != '0':
                    raise Exception('The alias of a starting room must be "0"')
                self.save()
                self.starting_room.world_state = self
                self.starting_room.save()

    def get_unique_room_id(self):
        id_to_serve = str(self._next_room_id)
        self._next_room_id = self._next_room_id + 1
        self.save()
        return id_to_serve

    def get_world(self):
        return next(world_module.World.objects(world_state=self))

    def add_custom_verb(self, custom_verb):
        self.custom_verbs.append(custom_verb)
        self.save()

    def clone(self):
        new_world_state = WorldState(_next_room_id=self._next_room_id, save_on_creation=False)

        new_world_state.starting_room = self.starting_room.clone()
        new_world_state.save()
        new_world_state.starting_room.world_state = new_world_state
        new_world_state.starting_room.save()

        for custom_verb in self.custom_verbs:
            new_world_state.custom_verbs.append(custom_verb.clone())

        for room in room_module.Room.objects(world_state=self, alias__ne=self.starting_room.alias):
            room.clone(new_world_state=new_world_state)

        cloned_rooms = room_module.Room.objects(world_state=new_world_state)
        exits_to_clone = [exit_to_clone for room in room_module.Room.objects(world_state=self) for exit_to_clone in room.exits]
        for exit in exits_to_clone:
            new_exit_location = next(filter(lambda r: r.alias==exit.room.alias, cloned_rooms))
            new_exit_destination = next(filter(lambda r: r.alias==exit.destination.alias, cloned_rooms))
            exit.clone(new_destination=new_exit_destination, new_room=new_exit_location)

        for inventory in inventory_module.Inventory.objects(world_state=self):
            inventory.clone(new_world_state=new_world_state)

        saved_items = item_module.Item.objects(saved_in=self)
        for saved_item in saved_items:
            cloned_item = saved_item.clone(new_item_id=saved_item.item_id, new_saved_in=new_world_state)

        new_world_state.save()
        return new_world_state

    def get_rooms(self):
        return room_module.Room.objects(world_state=self)

    def delete(self):
        for custom_verb in self.custom_verbs:
            custom_verb.delete()
        super().delete()