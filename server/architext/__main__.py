"""
Run this file to start your server. It does all initial setup and contains the game loop.
"""
import architext
import mongoengine
import telnetserver
import atexit


def database_connect(uri=None):
    """Connects to the mongodb database specified in docker-compose file,
    or a custom provided URI.
    """
    if uri:
        mongoengine.connect(host=uri)
    else:
        mongoengine.connect('architext', host='mud-db')

def client_ids_cleanup():
    """Cleans client connection id in the database, disconnecting everyone.
    """
    for user in architext.entities.User.objects(client_id__ne=None):
        user.disconnect()

def clear_database():
    architext.entities.User.drop_collection()
    architext.entities.Item.drop_collection()
    architext.entities.Room.drop_collection()
    architext.entities.CustomVerb.drop_collection()
    architext.entities.World.drop_collection()
    architext.entities.WorldState.drop_collection()
    architext.entities.WorldSnapshot.drop_collection()
    architext.entities.Exit.drop_collection()

if __name__ == "__main__":
    # Server setup starts here
    import sys, getopt, time

    connected_to_db = False
    
    # Sets up logger for main server logs
    logger = architext.util.setup_logger('server_logger', 'server.txt', console=True)

    # Process commmand line args
    command_line_args = sys.argv[1:]
    try:
       opts, args = getopt.getopt(command_line_args,"d:")
    except getopt.GetoptError:
        print("Usage: python server.py [-d mongo_db_database_uri]\nIf you don't specify an URI, will try to connect to default docker-compose db.")
        sys.exit(2)
    
    # Try to connect to user-provided db
    for opt, arg in opts:
        if opt == "-d":
            database_connect(arg)
            connected_to_db = True
    
    # If not connected yet, try to connect to the default db specified in the docker-compose file
    if not connected_to_db:
        database_connect()
        
    # Server creation for telnet communication
    server = telnetserver.TelnetServer(error_policy='ignore', port=2112)

    # Dict of current session. Keys are ids provided by TelnetServer, values are the user's Session object.
    sessions = {}

    # Ensure there isn't any connected players at this point.
    client_ids_cleanup()

    # Add exit handler: something that will be done when server stops
    atexit.register(lambda: logger.info('server stopped'))

    logger.info("server started")
    # Start game loop
    while True:
        try:
            server.update()  # get new events

            # Handle new connections
            for new_client in server.get_new_clients():
                sessions[new_client] = architext.session.Session(new_client, server)

            # Handle disconnects
            for disconnected_client in server.get_disconnected_clients():
                if disconnected_client in sessions:
                    ended_session = sessions.pop(disconnected_client)
                    ended_session.disconnect()

            # Let each session handle messages sent by his client
            for sender_client, message in server.get_messages():
                if sender_client in sessions:
                    session = sessions[sender_client]
                    if session.client_id is None:  # the session has disconnected by itself
                        sessions.pop(sender_client)
                    else:
                        session.process_message(message)

            # Sleep a bit. We don't want to be using 100% CPU time.
            time.sleep(0.2)
        except Exception as e:
            logger.exception('ERROR: ' + str(e))

