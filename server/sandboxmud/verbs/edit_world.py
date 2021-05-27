from . import verb
import textwrap
from .. import entities
import sandboxmud.strings as strings

class EditWorld(verb.Verb):
    command = _('editworld')
    permissions = verb.CREATOR

    def __init__(self, session):
        super().__init__(session)
        self.world = self.session.user.room.world_state.get_world()
        self.option_number = None
        self.current_process_function = self.process_first_message


    def process(self, message):
        if message == '/':
            self.session.send_to_client(strings.cancelled)
            self.finish_interaction()
        else:
            self.current_process_function(message)

    def process_first_message(self, message):
        title = _('Editing this world: "{world_name}"').format(world_name=self.world.name)
        body = _(
            'Enter the number of the value you want to edit.\n'
            '    0 - Name\n'
            '    1 - Make public/private'
            '    2 - Edit freedom'
        )
        out_message = strings.format(title, body, cancel=True)
        self.session.send_to_client(out_message)
        self.current_process_function = self.process_option_number

    def process_option_number(self, message):
        try:
            message = int(message)
        except ValueError:
            self.session.send_to_client(strings.not_a_number)
            return
        
        options = {
            0: {
                "out_message": _('Enter the new name:'),
                "next_process_function": self.process_new_world_name,
            },
            1: {
                "out_message": _(
                    'This world is {actual_value}.\n'
                    'Do you want to change it to {new_value}? [yes/no]'
                ).format(
                    actual_value=(strings.public if self.world.public else strings.private), 
                    new_value=(strings.public if not self.world.public else strings.private)
                ), 
                "next_process_function": self.process_public_choice,
            },
            2: {
                "out_message": _(
                    'Who should be able to edit the world?\n'
                    '    0 - All users.\n'
                    '    1 - Only you and your designated editors.'
                ),
                "next_process_function": self.process_edit_freedom_option,
            }
        }

        try:
            chosen_option = options[message]
        except KeyError:
            self.session.send_to_client(strings.wrong_value)
            return

        self.session.send_to_client(chosen_option["out_message"])
        self.current_process_function = chosen_option["next_process_function"]

    def process_new_world_name(self, message):
        if not message:
            self.session.send_to_client(strings.is_empty)
            return

        world = self.session.user.room.world_state.get_world()
        world.name = message
        world.save()
        self.finish_interaction()
        self.session.send_to_client(_("The name has been successfully changed."))
        return

    def process_public_choice(self, message):
        if message.lower() in strings.yes_input_options:
            try:
                self.world.toggle_public()
            except entities.PublicWorldLimitReached:
                self.session.send_to_client(_('You have reached the limit of public worlds in this server. Try to make another world private or ask the admin to increase your limit.'))
                self.finish_interaction()
                return
            self.session.send_to_client(_('This world is now {public_or_private}.').format(public_or_private=(strings.public if self.world.public else strings.private)))
            self.finish_interaction()
        elif message.lower() in strings.no_input_options:
            self.session.send_to_client(_('OK. The world remains {public_or_private}').format(public_or_private=(strings.public if self.world.public else strings.private)))
            self.finish_interaction()
        else:
            self.session.send_to_client(_('Please enter "yes" or "no".'))

    def process_edit_freedom_option(self, message):
        if message == '0':
            self.session.user.room.world_state.get_world().set_to_free_edition()
            self.session.send_to_client(_("Everybody can edit this world now."))
            self.finish_interaction()
        elif message == '1':
            self.session.user.room.world_state.get_world().set_to_privileged_edition()
            self.session.send_to_client(_("Only your designated editors and you can edit this world now."))
            self.finish_interaction()
        else:
            self.session.send_to_client(strings.wrong_value)