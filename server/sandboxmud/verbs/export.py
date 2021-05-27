from . import verb
from .. import entities
import json
import textwrap

class ExportWorld(verb.Verb):
    command = _("export")
    pretty_command = _("export pretty")
    permissions = verb.PRIVILEGED

    def process(self, message):
        world_state = self.session.user.room.world_state
        world_state_dict_representation = self.dump_world_state(world_state)
        if message == self.pretty_command:
            json_out = json.dumps(
                world_state_dict_representation, 
                indent=4,
                separators=(',', ': ')
            )
        else:
            json_out = json.dumps(world_state_dict_representation)
        header = _(
            'Your world:\n'
            '────────────────────────────────────────────────────────────\n'
        )
        footer = _(
            '────────────────────────────────────────────────────────────\n'
            '\n'
            'You have exported your actual world. Copy the text between the horizontal lines and save it anywhere.\n'
            'You can import this and any exported world at the lobby.'
        )
        self.session.send_to_client(header + json_out + footer)
        self.finish_interaction()

    def dump_item(self, item):
        custom_verbs = [self.dump_custom_verb(verb) for verb in item.custom_verbs]
        return {
            "item_id": item.item_id,
            "name": item.name,
            "description": item.description,
            "visible": item.visible,
            "custom_verbs": custom_verbs
        }

    def dump_custom_verb(self, custom_verb):
        return {
            "names":    custom_verb.names,
            "commands": custom_verb.commands,
        }

    def dump_exit(self, exit):
        return {
            "name": exit.name,
            "description": exit.description,
            "destination": exit.destination.alias,
            "room": exit.room.alias,
            "visible": exit.visible,
            "is_open": exit.is_open,
            "key_names": exit.key_names
        }

    def dump_room(self, room):
        custom_verbs = [self.dump_custom_verb(verb) for verb in room.custom_verbs]
        items = [self.dump_item(item) for item in entities.Item.objects(room=room)]
        return {
            "name": room.name,
            "alias": room.alias,
            "description": room.description,
            "custom_verbs": custom_verbs,
            "items": items
        }

    def dump_inventories(self, inventories):
        items = []
        for inventory in inventories:
            items += inventory.items
        return [self.dump_item(item) for item in items]

    def dump_world_state(self, world_state):
        starting_room = world_state.starting_room

        other_rooms = entities.Room.objects(world_state=world_state, alias__ne=starting_room.alias)
        other_rooms = [self.dump_room(room) for room in other_rooms]

        custom_verbs = [self.dump_custom_verb(verb) for verb in world_state.custom_verbs]

        exits = []
        for room in entities.Room.objects(world_state=world_state):
            exits += room.exits
        exits = [self.dump_exit(exit) for exit in exits]
 
        # all items in inventories are extracted to be placed at the importer inventory.
        inventories = entities.Inventory.objects(world_state=world_state)
        inventory = self.dump_inventories(inventories)

        saved_items = entities.Item.objects(saved_in=world_state)
        saved_items = [self.dump_item(item) for item in saved_items]

        return {
            "next_room_id": world_state._next_room_id,
            "starting_room": self.dump_room(starting_room),
            "other_rooms": other_rooms,
            "custom_verbs": custom_verbs,
            "exits": exits,
            "inventory": inventory,
            "saved_items": saved_items
        }