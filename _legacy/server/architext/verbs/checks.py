from . import verb
from .. import  session
import architext.util as util
import regex

class CheckForItem(verb.Verb):
    regex_command = True

    check_room_command         = _('if (?P<item_name>.+) in room')
    check_inv_command          = _('if (?P<item_name>.+) in inventory')
    check_room_and_inv_command = _('if (?P<item_name>.+) in room or inventory')
    command = [check_room_command, check_inv_command, check_room_and_inv_command]

    def __init__(self, session):
        super().__init__(session)        
        self.current_process_function = self.process_first_message
        self.item_name = None
        self.true_case_actions = []
        self.false_case_actions = []
        self.condition_to_check = None

    def process(self, message):
        self.current_process_function(message)

    def process_first_message(self, message):
        match = util.match(self.command, message)

        self.item_name = match['item_name']
        
        if match['pattern'] == self.check_room_command:
            condition = _('there is an item called {item_name} in this room').format(item_name=self.item_name)
            self.condition_to_check = self.item_name_is_at_room
        elif match['pattern'] == self.check_inv_command:
            condition = _('there is an item called {item_name} in your inventory').format(item_name=self.item_name)
            self.condition_to_check = self.item_name_is_at_inv
        elif match['pattern'] == self.check_room_and_inv_command:
            condition = _('there is an item called {item_name} in this room or your inventory').format(item_name=self.item_name)
            self.condition_to_check = self.item_name_is_at_room_or_inv

        self.session.send_to_client(_(
            'Write the actions to perform if {condition}.\n'
            'Each action should be preceded by an hyphen, as in:\n'
            '-go door\n\n'
            'Enter "-OK" to end.'
        ).format(condition=condition))
        self.current_process_function = self.process_true_case_action

    def process_true_case_action(self, message):
        if not message.startswith('-'):
            self.session.send_to_client(_('Action ignored. It should be preceded by "-".'))
            return
        
        message = message[1:]    

        if message in ['OK', 'ok', 'Ok', 'oK']:
            self.session.send_to_client(_('Received. Now do the same with the actions you want to perform if the condition is not met.'))
            self.current_process_function = self.process_false_case_action 
        elif message:
            self.true_case_actions.append(message)
        else:
            pass       
            
    def process_false_case_action(self, message):
        if not message.startswith('-'):
            self.session.send_to_client(_('Action ignored. It should be preceded by "-".'))
            return
        
        message = message[1:]

        if message in ['OK', 'ok', 'Ok', 'oK']:
            self.session.send_to_client(_('OK, lets run it!'))
            self.check_and_run()
            self.finish_interaction()
        elif message:
            self.false_case_actions.append(message)
        else:
            pass

    def check_and_run(self):
        if self.condition_to_check():
            self.run(self.true_case_actions, self.session)
        else:
            self.run(self.false_case_actions, self.session)

    def item_name_is_at_room(self):
        item_names = [item.name for item in self.session.user.room.items]
        return self.item_name in item_names

    def item_name_is_at_inv(self):
        if isinstance(self.session, session.GhostSession):
            working_session = self.session.creator_session
        else:
            working_session = self.session

        inventory = working_session.user.get_current_world_inventory()
        return self.item_name in [item.name for item in inventory.items]

    def item_name_is_at_room_or_inv(self):
        return self.item_name_is_at_room() or self.item_name_is_at_inv()

    @classmethod
    def run(cls, actions, session):
        previous_session_verb = session.current_verb
        session.current_verb = None
        for action in actions:
            session.process_message(action)
        session.current_verb = previous_session_verb
    


            

    
