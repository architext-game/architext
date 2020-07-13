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
        self.send_to_client("Estás conectado. ¿Cómo te llamas?\n\r")

    def disconnect(self):
        if self.user is not None:
            self.send_to_others_in_room("¡Whoop! {} se ha esfumado.".format(self.user.name))
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
        message_to_clients = '{} dice "{}"'.format(self.user.name, message)
        self.send_to_room(message_to_clients)

    def shout(self, message):
        for user in User.objects:
            self.server.send_message(user.client_id, '{} grita "{}"'.format(self.user.name, message))

    def show_help(self):
        help = (
"""Bienvenido a este mundo, donde tienes el poder de dar forma a la realidad.\r
Escribe "mirar" para mirar a tu alrededor.\r
Escribe "decir hola" para decir "hola" a quienes tengas cerca..\r
Escribe "gritar HOLA" para que te oiga todo el mundo.\r
Escribe "emote Hay un terremoto" para producir un mini terremoto en tu habitación.\r
Escribe "ir puerta" para cruzar una puerta.\r
Escribe "construir" para comenzar a construir una habitación adyacente a donde estás..\r
""")
        self.send_to_client(help)


    def show_current_room(self):
        self.user.room.reload()
        title = self.user.room.name
        description = self.user.room.description if self.user.room.description else "Esta sala no tiene descripción."
        if len(self.user.room.exits) > 0:
            exits = '    '+('\n\r    '.join(["<{}> lleva a {}".format(exit, room.name) for exit, room in self.user.room.exits.items()]))
            exits = "Salidas:\n\r{}    ".format(exits)
        else:
            exits = "No hay ningún camino para salir de esta habitación (pero podrías ser el primero en crear uno)."
        players_here = '\n\r'.join(['{} está aquí.'.format(user.name) for user in User.objects(room=self.user.room, client_id__ne=None) if user != self.user])
        message = "Estás en {}.\n\r{}\n\r{}\n\r{}".format(title, description, exits, players_here)
        self.send_to_client(message)

    def process_user_name(self, name):
        if User.objects(name=name):
            self.user = User.objects(name=name).first()
            self.user.connect(self.session_id)
            self.send_to_client("Bienvenido de nuevo {}.".format(name))
        else:
            lobby = Room.objects(name='lobby').first()
            self.user = User(name=name, room=lobby)
            self.user.connect(self.session_id)
            self.send_to_client('Bienvenido {}. Si es tu primera vez, escribe "ayuda" para ver una pequeña guía.'.format(name))

        self.send_to_others_in_room("¡Puf! {} apareció.".format(name))
        self.show_current_room()
        self.process_message = self.process_regular_command

    def go(self, exit):
        origin_room = self.user.room
        self.send_to_others_in_room("{} se marcha por {}.".format(self.user.name, exit))
        self.user.move(exit)
        there_exit = [exit for exit, room in self.user.room.exits.items() if room == origin_room][0]
        self.send_to_others_in_room("{} llega desde {}.".format(self.user.name, there_exit))
        self.show_current_room()

    def process_regular_command(self, message):
        first_word = ""
        rest = ""

        splitted_message = message.split(maxsplit=1)
        if len(splitted_message) == 2:
            first_word, rest = splitted_message
        elif len(splitted_message) == 1:
            first_word = splitted_message[0]
        
        if first_word == "":
            pass
        elif first_word == 'mirar':
            self.show_current_room()
        elif first_word == 'ir':
            exit = rest
            if exit in self.user.room.exits:
                self.go(exit)
            elif [exit in room_exit for room_exit in self.user.room.exits.keys()].count(True) == 1:
                for room_exit in self.user.room.exits.keys():
                    if exit in room_exit:
                        exit = room_exit
                self.go(exit)
            elif [exit in room_exit for room_exit in self.user.room.exits.keys()].count(True) > 1:
                self.send_to_client('Hay más de una salida con ese nombre. Sé más específico.')
            else:
                self.send_to_client("No puedes encontrar esa salida.")
        elif first_word == 'decir':
            self.say_in_room(rest)
        elif first_word == 'gritar':
            self.shout(rest)
        elif first_word == 'construir':
            self.send_to_client("Comienzas a construir una habitación. ¿Cómo quieres llamarla?")
            self.process_message = self.process_room_name
        elif first_word == 'ayuda':
            self.show_help()
        elif first_word == 'emote':
            self.send_to_room(rest)
        else:
            self.send_to_client("No te entiendo.")

    
    def process_room_name(self, message):
        if not message:
            self.send_to_client("Tienes que poner un nombre a tu habitación. Prueba otra vez.")
        else:
            self.current_interaction_state['new_room_name'] = message
            self.send_to_client("Ahora introduce una descripción para tu nueva sala, para que todo el mundo sepa cómo es.")
            self.process_message = self.process_room_description 

    def process_room_description(self, message):
        self.current_interaction_state['new_room_description'] = message
        current_room = self.user.room.name
        new_room = self.current_interaction_state['new_room_name']
        self.send_to_client("Cómo quieres llamar a la salida desde {} a {}?".format(current_room, new_room))
        self.process_message = self.process_here_exit_name 

    def process_here_exit_name(self, message):
        if not message:
            self.send_to_client("Tienes que poner un nombre a tu habitación. Prueba otra vez.")
        else:
            self.current_interaction_state['here_exit_name'] = message
            current_room = self.user.room.name
            new_room = self.current_interaction_state['new_room_name']
            self.send_to_client("Cómo quieres llamar a la salida desde {} a {}?".format(new_room, current_room))
            self.process_message = self.process_there_exit_name 

    def process_there_exit_name(self, message):
        if not message:
            self.send_to_client("Tienes que poner un nombre a tu habitación. Prueba otra vez.")
        else:
            self.current_interaction_state['there_exit_name'] = message
            self.user.room.create_adjacent_room(
                there_name = self.current_interaction_state['new_room_name'],
                there_description = self.current_interaction_state['new_room_description'],
                exit_from_here = self.current_interaction_state['here_exit_name'],
                exit_from_there = self.current_interaction_state['there_exit_name']
            )
            self.send_to_client("¡Enhorabuena! Tu nueva habitación está lista.")
            self.send_to_others_in_room("Los ojos de {} se ponen en blanco un momento. Una nueva salida aparece en la habitación.".format(self.user.name))
            self.process_message = self.process_regular_command


def database_connect(uri=None):
    if uri:
        mongoengine.connect(host=uri)
    else:
        mongoengine.connect('sandboxmud', host='mud-db')

def client_ids_cleanup():
    for user in User.objects(client_id__ne=None):
        user.disconnect()

if __name__ == "__main__":
    import sys, getopt

    command_line_args = sys.argv[1:]
    
    try:
       opts, args = getopt.getopt(command_line_args,"d:")
    except getopt.GetoptError:
        sys.exit(2)
    
    connected = False
    for opt, arg in opts:
        if opt == "-d":
            database_connect(arg)
            connected = True
    if not connected:
        database_connect()

    if not Room.objects(name='lobby'):
        lobby = Room(name='lobby', description='Esta es la semilla desde la que florece un nuevo mundo. Escribe ayuda si no sabes qué hacer.')


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
