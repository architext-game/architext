from . import verb
from .. import util
import sandboxmud.strings as strings

class MasterClose(verb.Verb):
    command = _("masterclose ")
    permissions = verb.PRIVILEGED

    def process(self, message):
        command_length = len(self.command)
        exit_name = message[command_length:]
        exit_to_close = util.name_to_entity(self.session, exit_name, substr_match=["room_exits"])

        if exit_to_close == "many":
            self.session.send_to_client(strings.many_found)
        elif exit_to_close is None:
            self.session.send_to_client(strings.not_found)
        else:
            exit_to_close.close()
            self.session.send_to_client(_('The exit "{exit_name}" has been closed.').format(exit_name=exit_to_close.name))

        self.finish_interaction()


class MasterOpen(verb.Verb):
    command = _("masteropen ")
    permissions = verb.PRIVILEGED

    def process(self, message):
        command_length = len(self.command)
        exit_name = message[command_length:]
        exit_to_open = util.name_to_entity(self.session, exit_name, substr_match=["room_exits"])

        if exit_to_open == "many":
            self.session.send_to_client(strings.many_found)
        elif exit_to_open is None:
            self.session.send_to_client(strings.not_found)
        else:
            exit_to_open.open()
            self.session.send_to_client(_('The exit "{exit_name}" is now open.').format(exit_name=exit_to_open.name))

        self.finish_interaction()


class AssignKey(verb.Verb):
    command = _("assignkey ")
    permissions = verb.PRIVILEGED

    def __init__(self, session):
        super().__init__(session)
        self.exit_to_assign = None
        self.current_process_function = self.process_exit_name

    def process(self, message):
        if message == '/':
            self.session.send_to_client(strings.cancelled)
            self.finish_interaction()
        else:
            self.current_process_function(message)

    def process_exit_name(self, message):
        command_length = len(self.command)
        exit_name = message[command_length:]
        self.exit_to_assign = util.name_to_entity(self.session, exit_name, substr_match=["room_exits"])

        if self.exit_to_assign == "many":
            self.session.send_to_client(strings.many_found)
            self.finish_interaction()
        elif self.exit_to_assign is None:
            self.session.send_to_client(strings.not_found)
            self.finish_interaction()
        else:
            self.current_process_function = self.process_item_name
            self.session.send_to_client(
                _('What is the name of the item that will open "{exit_name}"? ("/" to cancel)')
                    .format(exit_name=self.exit_to_assign.name)
            )

    def process_item_name(self, message):
        self.exit_to_assign.add_key(message)
        self.session.send_to_client(_("Key added."))
        self.finish_interaction()


class Open(verb.Verb):
    command = _("open ")

    def process(self, message):
        command_length = len(self.command)
        partial_exit_name = message[command_length:]
        selected_exit = util.name_to_entity(self.session, partial_exit_name, substr_match=["room_exits"])

        if selected_exit == "many":
            self.session.send_to_client(strings.many_found)
        elif selected_exit is None:
            self.session.send_to_client(strings.not_found)
        else:
            self.open(selected_exit)

        self.finish_interaction()

    def open(self, exit_to_open):
        if(exit_to_open.is_open):
            self.session.send_to_client(_('The exit "{exit_name}" is already open.').format(exit_name=exit_to_open.name))
            return

        for item in self.session.user.get_current_world_inventory().items:
            if item.name in exit_to_open.key_names:
                exit_to_open.open()
                self.session.send_to_client(_('You open {exit_name} using {key_name}.').format(exit_name=exit_to_open.name, key_name=item.name))
                return

        self.session.send_to_client(_('{exit_name}: You try to open it, but fail.').format(exit_name=exit_to_open.name))


class DeleteKey(verb.Verb):
    command = _("deletekey ")
    permissions = verb.PRIVILEGED

    def __init__(self, session):
        super().__init__(session)
        self.chosen_exit = None
        self.current_process_function = self.process_exit_name

    def process(self, message):
        if message == '/':
            self.session.send_to_client(strings.cancelled)
            self.finish_interaction()
        else:
            self.current_process_function(message)

    def process_exit_name(self, message):
        command_length = len(self.command)
        exit_name = message[command_length:]
        self.chosen_exit = util.name_to_entity(self.session, exit_name, substr_match=["room_exits"])

        if self.chosen_exit == "many":
            self.session.send_to_client(strings.many_found)
            self.finish_interaction()
        elif self.chosen_exit is None:
            self.session.send_to_client(strings.not_found)
            self.finish_interaction()
        else:
            if len(self.chosen_exit.key_names) > 0:
                out_message = _('{exit_name}: Which key do you want to remove?').format(exit_name=self.chosen_exit.name)
                for index, key in enumerate(self.chosen_exit.key_names):
                    out_message += f"\n    {index}. {key}"
                out_message += _("\n\n* To remove all assigned keys.")
                out_message += _("\n/ to cancel.")
                self.session.send_to_client(out_message)
                self.current_process_function = self.process_key_index
            else:
                self.session.send_to_client(_('The exit "{exit_name}" has no assigned keys.').format(exit_name=self.chosen_exit.name))
                self.finish_interaction()

    def process_key_index(self, message):
        if message == '*':
            keys_to_delete = self.chosen_exit.key_names.copy()
        else:
            try:
                index = int(message)
                if index < 0:
                    raise ValueError
            except ValueError:
                self.session.send_to_client(strings.not_a_number)
                return
            try:
                keys_to_delete = [ self.chosen_exit.key_names[index] ]
            except IndexError:
                self.session.send_to_client(strings.wrong_value)
                return

        for key_to_delete in keys_to_delete:
            self.chosen_exit.remove_key(key_to_delete)

        self.session.send_to_client(_('Key/s deleted.'))
        self.finish_interaction()


        



            