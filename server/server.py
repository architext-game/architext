import mongoengine
from entities import Room, User
from telnetserver import TelnetServer

class Session:
    def __init__(self, session_id, server):
        self.session_id   = session_id
        self.server = server
        self.process_message = self.process_user_name
        self.user = None
        self.current_interaction_state = {}
        self.send_to_client("You are connected. What is your name?\n\r")

    def disconnect(self):
        if self.user is not None:
            self.send_to_others_in_room("Whoop! {} has disappeared.".format(self.user.name))
            self.user.disconnect()

    def send_to_client(self, message):
        self.server.send_message(self.session_id, "\n\r"+message)

    def send_to_others_in_room(self, message):
        users_in_this_room = User.objects(room=self.user.room)
        for user in users_in_this_room:
            if user != self.user:
                self.server.send_message(user.client_id, message)

    def send_to_room(self, message):
        users_in_this_room = User.objects(room=self.user.room)
        for user in users_in_this_room:
            self.server.send_message(user.client_id, message)

    def say_in_room(self, message):
        message_to_clients = '{} says "{}"'.format(self.user.name, message)
        self.send_to_others_in_room(message_to_clients)

    def shout(self, message):
        for user in User.objects:
            self.server.send_message(user.client_id, '{} shouts "{}"'.format(self.user.name, message))

    def show_help(self):
        help = (
"""Welcome to this realm, where you have the power to shape reality.\r
Type "look" to look at your surroundings.\r
Type "say something" to communicate to people nearby.\r
Type "shout something" to communicate to everyone.\r
Type "emote something" to make something happen in your room.\r
Type "go exit" to travel trough an exit.\r
Type "build" to start building a room adjacent to your current location.\r
""")
        self.send_to_client(help)


    def show_current_room(self):
        title = self.user.room.name
        description = self.user.room.description if self.user.room.description else "This room has no description."
        if len(self.user.room.exits) > 0:
            exits = '    '+('\n\r    '.join(["<{}> leads to {}".format(exit, room.name) for exit, room in self.user.room.exits.items()]))
            exits = "Exits:\n\r{}    ".format(exits)
        else:
            exits = "There is no way to exit this room (but you may be the first to build it)."
        players_here = '\n\r'.join(['{} is here.'.format(user.name) for user in User.objects(room=self.user.room, client_id__ne=None) if user != self.user])
        message = "You are in {}.\n\r{}\n\r{}\n\r{}".format(title, description, exits, players_here)
        self.send_to_client(message)

    def process_user_name(self, name):
        if User.objects(name=name):
            self.user = User.objects(name=name).first()
            self.user.connect(self.session_id)
            self.send_to_client("Welcome back {}.".format(name))
        else:
            lobby = Room.objects(name='lobby').first()
            self.user = User(name=name, room=lobby)
            self.user.connect(self.session_id)
            self.send_to_client("Welcome {}".format(name))

        self.send_to_others_in_room("Puf! {} appears here.".format(name))
        self.show_current_room()
        self.process_message = self.process_regular_command

    def go(self, exit):
        origin_room = self.user.room
        self.send_to_others_in_room("{} leaves through {}.".format(self.user.name, exit))
        self.user.move(exit)
        there_exit = [exit for exit, room in self.user.room.exits.items() if room == origin_room][0]
        self.send_to_others_in_room("{} arrives from {}.".format(self.user.name, there_exit))
        self.show_current_room()

    def process_regular_command(self, message):
        splitted_message = message.split(maxsplit=1)
        if len(splitted_message) == 2:
            first_word, rest = splitted_message
        else:
            first_word = splitted_message[0]
            rest = ""
        
        if first_word == 'look':
            self.show_current_room()
        elif first_word == 'go':
            exit = rest
            if exit in self.user.room.exits:
                self.go(exit)
            elif [exit in room_exit for room_exit in self.user.room.exits.keys()].count(True) == 1:
                for room_exit in self.user.room.exits.keys():
                    if exit in room_exit:
                        exit = room_exit
                self.go(exit)
            elif [exit in room_exit for room_exit in self.user.room.exits.keys()].count(True) > 1:
                self.send_to_client('There is more than one exit with that name. Be more specific!')
            else:
                self.send_to_client("You can't find that exit.")
        elif first_word == 'say':
            self.say_in_room(rest)
        elif first_word == 'shout':
            self.shout(rest)
        elif first_word == 'build':
            self.send_to_client("Room building started! Enter the name of the new room.")
            self.process_message = self.process_room_name
        elif first_word == 'help':
            self.show_help()
        elif first_word == 'emote':
            self.send_to_room(rest)
        else:
            self.send_to_client("I don't understand that.")

    
    def process_room_name(self, message):
        if not message:
            self.send_to_client("You have to give your room a name!")
        else:
            self.current_interaction_state['new_room_name'] = message
            self.send_to_client("Now enter a description for your room")
            self.process_message = self.process_room_description 

    def process_room_description(self, message):
        self.current_interaction_state['new_room_description'] = message
        current_room = self.user.room.name
        new_room = self.current_interaction_state['new_room_name']
        self.send_to_client("How would you like to call the exit from {} to {}?".format(current_room, new_room))
        self.process_message = self.process_here_exit_name 

    def process_here_exit_name(self, message):
        if not message:
            self.send_to_client("You have to give it a name! Write it now.")
        else:
            self.current_interaction_state['here_exit_name'] = message
            current_room = self.user.room.name
            new_room = self.current_interaction_state['new_room_name']
            self.send_to_client("How would you like to call the exit from {} to {}?".format(new_room, current_room))
            self.process_message = self.process_there_exit_name 

    def process_there_exit_name(self, message):
        if not message:
            self.send_to_client("You have to give it a name! Write it now.")
        else:
            self.current_interaction_state['there_exit_name'] = message
            self.user.room.create_adjacent_room(
                there_name = self.current_interaction_state['new_room_name'],
                there_description = self.current_interaction_state['new_room_description'],
                exit_from_here = self.current_interaction_state['here_exit_name'],
                exit_from_there = self.current_interaction_state['there_exit_name']
            )
            self.send_to_client("Congrats! You have finished your new shiny room!")
            self.process_message = self.process_regular_command


def database_connect():
    mongoengine.connect('sandboxmud', host='mud-db')

def client_ids_cleanup():
    for user in User.objects(client_id__ne=None):
        user.disconnect()

if __name__ == "__main__":
    database_connect()

    if not Room.objects(name='lobby'):
        lobby = Room(name='lobby', description='This is where everything starts. Write "help" if you need guidance.')
        lobby.save()


    server = TelnetServer()
    sessions = {}

    client_ids_cleanup()

    while True:
        server.update()

        for new_client in server.get_new_clients():
            sessions[new_client] = Session(new_client, server)

        for disconnected_client in server.get_disconnected_clients():
            if disconnected_client in sessions:
                session = sessions.pop(disconnected_client)
                session.disconnect()
                
        # For each message a client has sent
        for sender_client, message in server.get_messages(): 
            if sender_client in sessions:
                sessions[sender_client].process_message(message)
