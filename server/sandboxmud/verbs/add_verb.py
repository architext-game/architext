from . import verb
from .. import entities
from .. import util
import functools
import textwrap
import sandboxmud.strings as strings

class AddVerb(verb.Verb):
    """This verb allows users to create new custom verbs tied to items.
    """

    item_command  = _('itemverb ')  # command for adding verbs to items
    room_command  = _('roomverb')   # command for adding verbs to rooms
    world_command = _('worldverb')  # command for adding verbs to worlds
    command = [item_command, room_command, world_command]
    permissions = verb.PRIVILEGED

    @classmethod
    def can_process(cls, message, session):
        if message.startswith(cls.item_command) or message.startswith(cls.room_command) or message.startswith(cls.world_command) and super().can_process(message, session):
            return True
        else:
            return False

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
        # figure out wether it is a world, room or item verb
        if message.startswith(self.item_command):
            self.process_item_name(message)
        elif message.startswith(self.room_command):
            self.process_room_verb_creation(message)
        elif message.startswith(self.world_command):
            self.process_world_verb_creation(message)
        else:
            raise ValueError('invalid message "{}"'.format(message))

    def process_item_name(self, message):
        name = message[len(self.item_command):]
        target_item = util.name_to_entity(self.session, name, loose_match=["saved_items"], substr_match=["room_items", "inventory"])

        if target_item == "many":
            self.session.send_to_client(strings.many_found)
            self.finish_interaction()
        elif target_item is None:
            self.session.send_to_client(strings.not_found)
            self.finish_interaction()
        else:
            self.item = target_item
            self.current_process_function = self.process_verb_names

            body = textwrap.dedent(_("""\
                You are creating a verb that any player will be able to use over this item.

                Now enter the verb's name. If you write "use" the verb will be executed by "use {item_name}".
                You can give the verb multiple names. Just enter all of them separated by a whitespace.

                Verb name/s:"""
            ).format(item_name=self.item.name))
            
            if target_item.is_saved():
                title = _('Adding verb to saved item "{item_id}"').format(item_id=self.item.item_id)
                self.session.send_to_client(strings.format(title, body, cancel=True))

            else:
                title = _('Adding verb to item "{item_id}"').format(item_id=self.item.name)
                self.session.send_to_client(strings.format(title, body, cancel=True))


    def process_room_verb_creation(self, message):
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

    def process_world_verb_creation(self, message):
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
        if message in ['OK', 'ok'] and len(self.command_list) > 0:
            self.build_verb()
            self.finish_interaction()
        elif self.is_valid_command(message):
            self.command_list.append(message)
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
    item_command = _('seeitemverb ')
    world_command = _('seeworldverb')
    room_command = _('seeroomverb')
    command = [item_command, world_command, room_command]

    def process(self, message):
        out_message = ""
        
        if message == self.world_command:
            self.inspectable_custom_verbs = self.session.user.room.world_state.custom_verbs
        elif message == self.room_command:
            self.inspectable_custom_verbs = self.session.user.room.custom_verbs
        else:
            item_name = message[len(self.item_command):]
            selected_item = util.name_to_entity(self.session, item_name, loose_match=["saved_items"], substr_match=["room_items", "inventory"])

            if selected_item == "many":
                self.session.send_to_client(strings.many_found)
                self.finish_interaction()
                return
            elif selected_item is None:
                self.session.send_to_client(strings.not_found)
                self.finish_interaction()
                return
            else:
                self.inspectable_custom_verbs = selected_item.custom_verbs
                if selected_item.is_saved():
                    out_message += _("Saved item: {item_id}\n").format(item_id=selected_item.item_id)
                else:
                    out_message += _("Item: {item_name}\n").format(item_name=selected_item.name)
                    
        
        if not self.inspectable_custom_verbs:
            out_message += _("There are no verbs to show.")
            self.session.send_to_client(out_message)
            self.finish_interaction()
            return

        out_message += _('Which verb do you want to see?\n')
        out_message += self.get_custom_verb_list()
        self.session.send_to_client(out_message)
        self.process = self.process_menu_option


    def get_custom_verb_list(self):
        list = ''
        for index, custom_verb in enumerate(self.inspectable_custom_verbs):
            list += '{}. {}\n'.format(index, custom_verb.names)
        list += _('\n\n"/" to cancel')
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
    item_command  = _('deleteitemverb ')
    room_command  = _('deleteroomverb')
    world_command = _('deleteworldverb')
    command = [item_command, room_command, world_command]
    permissions = verb.PRIVILEGED

    def process(self, message):
        if message == self.world_command:
            self.deletable_custom_verbs = self.session.user.room.world_state.custom_verbs
            target_name = _('this world')
        elif message == self.room_command:
            self.deletable_custom_verbs = self.session.user.room.custom_verbs
            target_name = _('"{room_name}" (room)').format(room_name=self.session.user.room.name)
        else:
            item_name = message[len(self.item_command):]

            selected_item = util.name_to_entity(self.session, item_name, loose_match=["saved_items"], substr_match=["room_items", "inventory"])

            if selected_item == "many":
                self.session.send_to_client(strings.many_found)
                self.finish_interaction()
                return
            elif selected_item is None:
                self.session.send_to_client(strings.not_found)
                self.finish_interaction()
                return
            target_name = (
                _('"{item_id}" (saved item)').format(item_id=selected_item.item_id)
                if selected_item.is_saved()
                else _('"{item_name}" (item)').format(item_name=selected_item.name)
            )
            self.deletable_custom_verbs = selected_item.custom_verbs

        if not self.deletable_custom_verbs:
            self.session.send_to_client(_("{target_name} has no verbs to delete.").format(target_name=target_name))
            self.finish_interaction()
            return

        title = _("Deleting verb of {target_name}").format(target_name=target_name)
        body  = _("Enter the number of the verb to delete.\n{verb_list}").format(target_name=target_name, verb_list=self.get_custom_verb_list())
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
        

