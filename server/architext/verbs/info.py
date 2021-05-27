import functools
import textwrap
from . import verb
from .. import util
from .. import entities
import architext.strings as strings

class WorldInfo(verb.Verb):
    command = _('worldinfo')

    def process(self, message):
        self.show_world_info()
        self.finish_interaction()

    def show_world_info(self):
        world = self.session.user.room.world_state.get_world()
        
        if world.editors:
            editor_names = functools.reduce(lambda a,b: '{}, {}'.format(a,b), [editor.name for editor in world.editors])
        else:
            editor_names = _('No one.')
        message = _(
            'Name: {world_name}\n'
            'Creator: {creator_name}\n'
            'Editors: {editor_names}\n'
            'Free edition: {all_can_edit}\n'
            'This world is {public_or_private}\n'
            'Invitation code: {world_id}'
        ).format(
            world_name=world.name,
            creator_name=world.creator.name,
            editor_names=editor_names,
            all_can_edit=world.all_can_edit,
            public_or_private=strings.public if world.public else strings.private,
            world_id=world.id,
        )
        self.session.send_to_client(message)


class Info(verb.Verb):
    """Shows all info of a room or item. This command is designed for creators, since it shows
    info that should be secret."""

    command = _('info')
    permissions = verb.PRIVILEGED

    def process(self, message):
        command_length = len(self.command) + 1
        if message[command_length:]:
            self.show_item_info(message[command_length:])
        else:
            self.show_current_room_info()
        self.finish_interaction()

    def show_item_info(self, partial_item_name):
        selected_entity = util.name_to_entity(self.session, partial_item_name, loose_match=['saved_items'], substr_match=['room_items', 'inventory', 'room_exits'])

        if selected_entity == "many":
            self.session.send_to_client(strings.many_found)
            self.finish_interaction()
        elif selected_entity is None:
            self.session.send_to_client(strings.not_found)
            self.finish_interaction()
        else:
            if isinstance(selected_entity, entities.Item):
                self.session.send_to_client(_(
                    'Item name "{item_name}"\n'
                    'Description: "{description}"\n'
                    'Visibility: {visible}'
                ).format(item_name=selected_entity.name, description=selected_entity.description, visible=selected_entity.visible))
            elif isinstance(selected_entity, entities.Exit):
                self.session.send_to_client(_(
                    'Exit name: "{exit_name}"\n'
                    'Description "{description}"\n'
                    'Visibility: {visible}\n'
                    'Destination: {destination_name} (number {destination_alias})'
                ).format(
                    exit_name=selected_entity.name, 
                    description=selected_entity.description, 
                    visible=selected_entity.visible,
                    destination_name=selected_entity.destination.name,
                    destination_alias=selected_entity.destination.alias
                ))
            else:
                raise ValueError(f"Item or Exit expected. {type(selected_entity)} found.")

    
    def show_current_room_info(self):
        room_name = self.session.user.room.name
        description = self.session.user.room.description
        alias = self.session.user.room.alias

        exit_list = []
        for exit in self.session.user.room.exits:
            exit_list.append(
                _('   "{exit_name}" lleva a "{destination_name}" number {destination_alias} ({exit_visibility})')
                    .format(
                        exit_name=exit.name, 
                        destination_name=exit.destination.name, 
                        destination_alias=exit.destination.alias,
                        exit_visibility=self.visible_output(exit)
                    )
            )
        exit_string = '\n'.join(exit_list)

        item_list = []
        for item in self.session.user.room.items:
            item_list.append(f'   {item.name} ({self.visible_output(item)})')
        item_string = '\n'.join(item_list)
        
        players_online = ', '.join(['{}'.format(user.name) for user in entities.User.objects(room=self.session.user.room, client_id__ne=None)])
        players_offline = ', '.join(['{}'.format(user.name) for user in entities.User.objects(room=self.session.user.room, client_id=None)])
        title = _('Room "{room_name}"').format(room_name=room_name)
        body = _(
            'Room number: {alias}\n'
            'Description: {description}\n'
            'Exits:\n'
            '{exit_string}\n'
            'Items:\n'
            '{item_string}\n'
            'Online players here: {players_online}\n'
            'Offline players here: {players_offline}'
        ).format(
            alias=alias,
            description=description,
            exit_string=exit_string,
            item_string=item_string,
            players_online=players_online,
            players_offline=players_offline,
        )
        out_message = strings.format(title, body)
        self.session.send_to_client(out_message)

    def visible_output(self, item):
        if item.visible == 'takable':
            return _('takable')
        if item.visible=='obvious':
            return _('visible')
        if item.visible=='listed':
            return _('listed')
        if item.visible=='hidden':
            return _('hidden')