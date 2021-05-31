from . import verb
from .. import entities
from .. import util
import functools
import textwrap
import architext.strings as strings
import re

class AddVerb(verb.Verb):
    """This verb allows users to create new custom verbs tied to items.
    """

    command  = _('verb ')
    room_special_name  = _('room')   # special_name for adding verbs to rooms
    room_alt_name  = _('*room*')
    world_special_name = _('world')  # special_name for adding verbs to worlds
    world_alt_name  = _('*world*')
    permissions = verb.PRIVILEGED

    def __init__(self, session):
        super().__init__(session)
        self.world_state = None  # world on which the verb will be added, if it is a world verb
        self.room = None   # room  on which the verb will be added, if it is a room verb
        self.item = None   # item  on which the verb will be added, if it is a item verb
        self.verb_names = None
        self.command_list = []
        self.current_process_function = self.process_first_message

    def process(self, message):
        if message == '/':
            self.session.send_to_client(strings.cancelled)
            self.finish_interaction()
        else:
            self.current_process_function(message)

    def process_first_message(self, message):
        name = message[len(self.command):]
        target_item = util.name_to_entity(self.session, name, loose_match=["saved_items"], substr_match=["room_items", "inventory"])

        if target_item is not None and name in [self.room_special_name, self.world_special_name]:
            if name == self.room_special_name:
                self.session.send_to_client(_('🚧 🚧 🚧 🚧 🚧 🚧\nNote: An item with that name was found. If you want to add the verb to the room instead, you can use "addverb *room*"'))
            if name == self.world_special_name:
                self.session.send_to_client(_('🚧 🚧 🚧 🚧 🚧 🚧\nNote: An item with that name was found. If you want to add the verb to the world instead, you can use "addverb *world*"'))

        if target_item == "many":
            self.session.send_to_client(strings.many_found)
            self.finish_interaction()
        elif target_item is not None:
            self.process_item_verb_creation(target_item)
        elif name == self.room_special_name or name == self.room_alt_name:
            self.process_room_verb_creation()
        elif name == self.world_special_name or name == self.world_alt_name:
            self.process_world_verb_creation()

    def process_item_verb_creation(self, target_item):
        self.item = target_item

        body = textwrap.dedent(_("""\
            You are creating a verb that any player will be able to use over this item.

            Now enter the verb's name. If you write "use" the verb will be executed by "use {item_name}".
            You can give the verb multiple names. Just enter all of them separated by a whitespace.

            Verb name/s:"""
        ).format(item_name=self.item.name))
        
        if target_item.is_saved():
            title = _('Adding verb to saved item "{item_id}"').format(item_id=self.item.item_id)
        else:
            title = _('Adding verb to item "{item_id}"').format(item_id=self.item.name)

        self.session.send_to_client(strings.format(title, body, cancel=True))
        self.current_process_function = self.process_verb_names

    def process_room_verb_creation(self):
        self.room = self.session.user.room
        title = _('Adding verb to this room')
        body = textwrap.dedent(_("""\
            You are creating a verb that any player in this room will be able to use.

            Now enter the verb's name. If you write "sing" the verb will be executed simply by "sing".
            You can give the verb multiple names. Just enter all of them separated by a whitespace.

            Verb name/s:"""
        ))
        self.session.send_to_client(strings.format(title, body, cancel=True))
        self.current_process_function = self.process_verb_names

    def process_world_verb_creation(self):
        self.world_state = self.session.user.room.world_state
        title = _('Adding verb to this world')
        body = textwrap.dedent(_("""\
            You are creating a verb that any player in this world will be able to use.

            Now enter the verb's name. If you write "sing" the verb will be executed simply by "sing".
            You can give the verb multiple names. Just enter all of them separated by a whitespace.

            Verb name/s:"""
        ))
        self.session.send_to_client(strings.format(title, body, cancel=True))
        self.current_process_function = self.process_verb_names

    def process_verb_names(self, message):
        verb_names = message.split()
        if len(verb_names) == 0:
            self.session.send_to_client(strings.is_empty)
            return
        for name in verb_names:
            if not self.is_valid_verb_name(message):                
                self.session.send_to_client(_("One of your verb names is invalid. Try again."))
                return
        self.verb_names = verb_names
        out_message = textwrap.dedent(_('''\
            Verb actions
            ────────────
            Now write the actions to perform when the verb is executed.
              ● You can use any action that you would normally do as a player or editor.
              ● When the verb is used, an invisible ghost player will perform the actions you provided.
              ● If you write "{user_name_placeholder}" in any action, it will be substituted by the name of the player that used the verb.
              
            You can write as many actions as you like, one per line, as you would do while playing. You won't see any answer to your commands. When you are finished, write "OK".
              
            Verb actions: ("OK" to finish)''').format(user_name_placeholder=strings.user_name_placeholder))
        self.session.send_to_client(out_message)
        self.current_process_function = self.process_command

    def process_command(self, message):
        commands = re.split(r';\r\n|;\n', message)

        if '\n' in message and len(commands)==1:
            self.session.send_to_client(_('Note: your multiline message will be treated as one single command. If you want to send multiple commands in one message, write ";" at the end of each of them.'))
        
        # remove trailing ";"
        if len(commands) > 0 and len(commands[-1]) > 0 and commands[-1][-1] == ';':
            commands[-1] = commands[-1][0:-1]

        for command in commands:
            if command.lower() == 'ok' and len(self.command_list) > 0:
                self.build_verb()
                self.finish_interaction()
            elif self.is_valid_command(command):
                self.command_list.append(command)
            else:
                self.session.send_to_client(_("That last command is invalid. It has been ignored."))

    def build_verb(self):
        new_verb = entities.CustomVerb(names=self.verb_names, commands=self.command_list)
        if self.item is not None:
            self.item.add_custom_verb(new_verb)
            self.session.send_to_client(_('Verb created. Write "{verb_name} {item_name}" to unleash its power!').format(verb_name=self.verb_names[0], item_name=self.item.name))
        elif self.room is not None:
            self.room.add_custom_verb(new_verb)
            self.session.send_to_client(_('Room verb created. Write "{verb_name}" to unleash its power!').format(verb_name=self.verb_names[0]))
        elif self.world_state is not None:
            self.world_state.add_custom_verb(new_verb)
            self.session.send_to_client(_('World verb created. Write "{verb_name}" to unleash its power!').format(verb_name=self.verb_names[0]))
        else:
            raise RuntimeError("Unreachable code reached ¯\_(ツ)_/¯")

    def is_valid_verb_name(self, name):
        # TODO checks if a name is a valid verb name
        return True

    def is_valid_command(self, command):
        if not command:
            return False
        return True

class InspectCustomVerb(verb.Verb):
    command = _('seeverbs ')
    room_special_name  = _('room')   # special_name for adding verbs to rooms
    room_alt_name  = _('*room*')
    world_special_name = _('world')  # special_name for adding verbs to worlds
    world_alt_name  = _('*world*')

    def process(self, message):
        title = ""
        body = ""

        name = message[len(self.command):]
        target_item = util.name_to_entity(self.session, name, loose_match=["saved_items"], substr_match=["room_items", "inventory"])

        if target_item is not None and name in [self.room_special_name, self.world_special_name]:
            if name == self.room_special_name:
                self.session.send_to_client(_('🚧 🚧 🚧 🚧 🚧 🚧\nNote: An item with that name was found. If you want to see the the room verbs instead, you can use "seeverbs *room*"'))
            if name == self.world_special_name:
                self.session.send_to_client(_('🚧 🚧 🚧 🚧 🚧 🚧\nNote: An item with that name was found. If you want to see the the world verbs instead, you can use "seeverbs *world*"'))

        if target_item == "many":
            self.session.send_to_client(strings.many_found)
            self.finish_interaction()
            return
        elif target_item is not None:
            self.inspectable_custom_verbs = target_item.custom_verbs
            if target_item.is_saved():
                title = _('Verbs of saved item "{item_id}"').format(item_id=target_item.item_id)
            else:
                title = _('Verbs of item "{item_name}"').format(item_name=target_item.name)
        elif name == self.room_special_name or name == self.room_alt_name:
            title = _("Verbs of room: {room_name}").format(room_name=self.session.user.room.name)
            self.inspectable_custom_verbs = self.session.user.room.custom_verbs
        elif name == self.world_special_name or name == self.world_alt_name:
            title = _("World-level verbs")
            self.inspectable_custom_verbs = self.session.user.room.world_state.custom_verbs

        if not self.inspectable_custom_verbs:
            body = _("There are no verbs to show.")
            self.session.send_to_client(strings.format(title, body))
            self.finish_interaction()
        else:
            body = self.get_custom_verb_list()
            body += _("\n ᐅ Enter the number of a verb to show its commands")
            self.session.send_to_client(strings.format(title, body, cancel=True))
            self.process = self.process_menu_option


    def get_custom_verb_list(self):
        list = ''
        for index, custom_verb in enumerate(self.inspectable_custom_verbs):
            list += '{}. {}\n'.format(index, custom_verb.names)
        return list

    def process_menu_option(self, message):
        if message == '/':
            self.session.send_to_client(strings.cancelled)
            self.finish_interaction()
            return

        try:
            index = int(message)
            if index < 0:
                raise ValueError
        except ValueError:
            self.session.send_to_client(_("Please enter a number."))
            return

        try:
            chosen_custom_verb = self.inspectable_custom_verbs[index]
        except IndexError:
            self.session.send_to_client(_("Please introduce the number of one of the listed verbs."))
            return

        message = functools.reduce(lambda a,b: '{} / {}'.format(a,b), chosen_custom_verb.names).upper() + "\n"
        message += functools.reduce(lambda a, b: '{}\n{}'.format(a,b), chosen_custom_verb.commands)
        message += '\nOK'
        self.session.send_to_client(message)
        self.finish_interaction()

class DeleteCustomVerb(verb.Verb):
    command = _('deleteverb ')
    room_special_name  = _('room')   # special_name for adding verbs to rooms
    room_alt_name  = _('*room*')
    world_special_name = _('world')  # special_name for adding verbs to worlds
    world_alt_name  = _('*world*')
    permissions = verb.PRIVILEGED

    def process(self, message):
        item_name = message[len(self.command):]
        selected_item = util.name_to_entity(self.session, item_name, loose_match=["saved_items"], substr_match=["room_items", "inventory"])
        
        if selected_item is not None and item_name in [self.room_special_name, self.world_special_name]:
            if item_name == self.room_special_name:
                self.session.send_to_client(_('🚧 🚧 🚧 🚧 🚧 🚧\nNote: An item with that name was found. If you want to delete the the room verbs instead, you can use "deleteverb *room*"'))
            if item_name == self.world_special_name:
                self.session.send_to_client(_('🚧 🚧 🚧 🚧 🚧 🚧\nNote: An item with that name was found. If you want to delete the the world verbs instead, you can use "deleteverb *world*"'))

        if selected_item == "many":
            self.session.send_to_client(strings.many_found)
            self.finish_interaction()
            return
        elif selected_item is not None:
            target_name = (
                _('"{item_id}" (saved item)').format(item_id=selected_item.item_id)
                if selected_item.is_saved()
                else _('"{item_name}" (item)').format(item_name=selected_item.name)
            )
            self.deletable_custom_verbs = selected_item.custom_verbs
        elif item_name == self.room_special_name or item_name == self.room_alt_name:
            self.deletable_custom_verbs = self.session.user.room.custom_verbs
            target_name = _('"{room_name}" (room)').format(room_name=self.session.user.room.name)
        elif item_name == self.world_special_name or item_name == self.world_alt_name:
            self.deletable_custom_verbs = self.session.user.room.world_state.custom_verbs
            target_name = _('this world')
        else:
            self.session.send_to_client(strings.not_found)
            self.finish_interaction()
            return

        if not self.deletable_custom_verbs:
            self.session.send_to_client(_("{target_name} has no verbs to delete.").format(target_name=target_name))
            self.finish_interaction()
            return

        title = _("Deleting verb of {target_name}").format(target_name=target_name)
        body  = _("{verb_list}\n ᐅ Enter the number of the verb to delete:").format(target_name=target_name, verb_list=self.get_custom_verb_list())
        out_message = strings.format(title, body, cancel=True)
        self.session.send_to_client(out_message)
        self.process = self.process_menu_option

    def get_custom_verb_list(self):
        list = ''
        for index, custom_verb in enumerate(self.deletable_custom_verbs):
            list += f' {index} - {custom_verb.names}\n'
        return list

    def process_menu_option(self, message):
        if message == '/':
            self.session.send_to_client(strings.cancelled)
            self.finish_interaction()
            return

        try:
            index = int(message)
            if index < 0:
                raise ValueError
        except ValueError:
            self.session.send_to_client(_("Please enter a number"))
            return

        try:
            chosen_custom_verb = self.deletable_custom_verbs[index]
        except IndexError:
            self.session.send_to_client(_("Please introduce the number of one of the listed verbs."))
            return

        chosen_custom_verb.delete()
        self.session.send_to_client(_('The verb has been deleted.'))
        self.finish_interaction()
        

