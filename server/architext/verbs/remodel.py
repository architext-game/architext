# Issue: directly changes room values, and calls save() method.

from . import verb
import architext.strings as strings
from architext.adapters.sender import MessageOptions

class Remodel(verb.Verb):
    """Lets players edit every aspect of a room"""

    command = _('reform')
    permissions = verb.PRIVILEGED

    def __init__(self, session):
        super().__init__(session)
        self.option_number = None
        self.current_process_function = self.process_first_message

    def process(self, message):
        if message == '/':
            self.session.send_to_client(strings.cancelled)
            self.finish_interaction()
        else:
            self.current_process_function(message)

    def process_first_message(self, message):
        title = _('Reforming room "{room_name}"').format(room_name=self.session.user.room.name)
        body  = _(
            'Enter the number of the field to modify\n'
            '    1 - Name\n'
            '    2 - Description'
        ) 
        self.session.send_formatted(title, body, cancel=True)
        self.current_process_function = self.process_reform_option

    def process_reform_option(self, message):
        try:
            message = int(message)
        except:
            self.session.send_to_client(strings.not_a_number)
            return

        if message == 1:
            self.option_number = message
            self.session.send_to_client(_('Enter the new name'), options=MessageOptions(fillInput=self.session.user.room.name))
            self.current_process_function = self.process_reform_value
        elif message == 2:
            self.option_number = message
            self.session.send_to_client(_('Enter the new description'), options=MessageOptions(fillInput=self.session.user.room.description))
            self.current_process_function = self.process_reform_value
        else:
            self.session.send_to_client(strings.wrong_value)
        
    def process_reform_value(self, message): 
        option = self.option_number
        if message:
            if option == 1:
                self.session.user.room.name = message
            elif option == 2:
                self.session.user.room.description = message
            self.session.user.room.save()
            self.session.send_to_client(_('Reform completed.'))
            self.finish_interaction()
        else:
            self.session.send_to_client(strings.is_empty)