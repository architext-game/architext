import socketio
from architext.session import Session
from architext.adapters.sender import SocketIOSender
import typing
import architext
import mongoengine
import atexit
import os
from dotenv import load_dotenv

def database_connect(uri=None):
    """Connects to the mongodb database specified in docker-compose file,
    or a custom provided URI.
    """
    if uri:
        mongoengine.connect(host=uri)
    else:
        database = os.getenv('DATABASE', default='architext')
        host     = host=os.environ['DB_HOST']
        mongoengine.connect(database, host=host)

def client_ids_cleanup():
    """Cleans client connection id in the database, disconnecting everyone.
    """
    for user in architext.entities.User.objects(client_id__ne=None):
        user.disconnect()

if __name__ == "__main__":
    # Server setup starts here
    import sys, getopt, time

    load_dotenv()

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
        

    # Dict of current session. Keys are ids provided by TelnetServer, values are the user's Session object.
    sessions = {}

    # Ensure there isn't any connected players at this point.
    client_ids_cleanup()

    # Add exit handler: something that will be done when server stops
    atexit.register(lambda: logger.info('server stopped'))

    sio = socketio.Server(cors_allowed_origins=os.getenv('CLIENT_URL', default='*'))

    sessions: typing.Dict[str, Session] = {}
    userid_to_sid: typing.Dict[str, str] = {}

    def get_sid(user_id):
        return userid_to_sid[user_id]

    @sio.event
    def connect(sid, environ):
        sender = SocketIOSender(sio=sio)
        sessions[sid] = Session(sender=sender, client_id=sid)
        logger.info(f'New connection, client_id {sid}')

    @sio.event
    def message(sid, data):
        if sid in sessions:
            session = sessions[sid]
            if session.client_id is None:  # the session has disconnected by itself
                sessions.pop(sid)
            else:
                session.process_message(data)

    @sio.event
    def disconnect(sid):
        if sid in sessions:
            ended_session = sessions.pop(sid)
            if ended_session.user:
                logger.info(f'{ended_session.user.name} has disconnected.')
            else:
                logger.info(f'Disconnected before login: client_id {sid}')
            ended_session.disconnect()

    # Create a simple server application
    app = socketio.WSGIApp(sio)

    # Use eventlet or gevent for asynchronous server
    import eventlet
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
