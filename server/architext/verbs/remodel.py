# Issue: directly changes room values, and calls save() method.

from . import verb
import architext.strings as strings
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
            '    0 - Name\n'
            '    1 - Description'
        ) 
        self.session.send_to_client(strings.format(title, body, cancel=True))
        self.current_process_function = self.process_reform_option

    def process_reform_option(self, message):
        try:
            message = int(message)
        except:
            self.session.send_to_client(strings.not_a_number)
            return

        max_number = 1
        if 0 <= message <= max_number:
            self.option_number = message
            self.session.send_to_client(_('Enter the new value'))
            self.current_process_function = self.process_reform_value
        else:
            self.session.send_to_client(strings.wrong_value)
        
    def process_reform_value(self, message): 
        option = self.option_number
        if message:
            if option == 0:
                self.session.user.room.name = message
            elif option == 1:
                self.session.user.room.description = message
            self.session.user.room.save()
            self.session.send_to_client(_('Reform completed.'))
            self.finish_interaction()
        else:
            self.session.send_to_client(strings.is_empty)