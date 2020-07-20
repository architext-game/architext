import mongoengine
from telnetserver import TelnetServer
from entities import Room, User, World, Item
import verbs as v

class Session:
    verbs = [v.Build, v.Emote, v.Go, v.Help, v.Login, v.Look, v.Remodel, v.Say, v.Shout, v.Craft, v.EditItem, v.Connect, v.Teleport, v.DeleteRoom, v.DeleteItem, v.DeleteExit]

    def __init__(self, session_id, server):
        self.session_id   = session_id
        self.server = server
        self.current_verb = v.Login(self)
        self.user = None
        self.send_to_client("Estás conectado. ¿Cómo te llamas?\n\r")

    def process_message(self, message):
        if self.current_verb is None:
            for verb in self.verbs:
                if verb.can_process(message):
                    self.current_verb = verb(self)
                    break

        if self.current_verb is not None:
            self.current_verb.process(message)
            if self.current_verb.command_finished():
                self.current_verb = None
        else:
            self.send_to_client("No te entiendo.")

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

    def send_to_all(self, message):
        for user in User.objects:
            self.server.send_message(user.client_id, message)



def database_connect(uri=None):
    if uri:
        mongoengine.connect(host=uri)
    else:
        mongoengine.connect('sandboxmud', host='mud-db')

def client_ids_cleanup():
    for user in User.objects(client_id__ne=None):
        user.disconnect()

if __name__ == "__main__":
    import sys, getopt, time

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

    if not World.objects:
        Item.drop_collection()
        User.drop_collection()
        Room.drop_collection()
        new_world = World()

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

        time.sleep(0.2)
