from . import verb
from .. import  session

class CheckForItem(verb.Verb):
    command = 'si hay en '
    check_room_command = 'si hay en sala '
    check_inv_command =  'si hay en inventario '
    check_room_and_inv_command = 'si hay en sala o inventario '

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
        if message.startswith(self.check_room_command):
            self.item_name = message[len(self.check_room_command):]
            condition = 'un objeto llamado "{}" está en la sala'.format(self.item_name)
            self.condition_to_check = self.item_name_is_at_room
        elif message.startswith(self.check_inv_command):
            self.item_name = message[len(self.check_inv_command):]
            condition = 'un objeto llamado "{}" está en tu inventario'.format(self.item_name)
            self.condition_to_check = self.item_name_is_at_inv
        elif message.startswith(self.check_room_and_inv_command):
            self.item_name = message[len(self.check_room_and_inv_command):]
            condition = 'un objeto llamado "{}" está en la sala o en tu inventario.'.format(self.item_name)
            self.condition_to_check = self.item_name_is_at_room_or_inv
        else:
            self.session.send_to_client('No te entiendo')
            self.finish_interaction()
            return

        self.session.send_to_client('Introduce la secuencia de acciones que quieres realizar si {}\nCada acción debe estar precedida por un guión ("-").\nPara terminar, introduce OK, también precedido por un guión.'.format(condition))
        self.current_process_function = self.process_true_case_action

    def process_true_case_action(self, message):
        if message.startswith('-'):
                message = message[1:]

        if message in ['OK', 'ok']:
            self.session.send_to_client('OK, ahora haz lo mismo con las acciones a realizar si no se cumple la condición')
            self.current_process_function = self.process_false_case_action 
        elif message:
            self.true_case_actions.append(message)
        else:
            pass       
            
    def process_false_case_action(self, message):
        if message.startswith('-'):
                message = message[1:]

        if message in ['OK', 'ok']:
            self.session.send_to_client('Vale, VAMOS A HACERLO!')
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
    


            

    
