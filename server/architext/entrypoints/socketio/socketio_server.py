import socketio
import architext

# create a Socket.IO server
sio = socketio.Server()

sessions = {}

@sio.event
def user_message(sid, data):
    session = sessions.get(sid)
    if not session:
        sessions[sid] = architext.session.Session(new_client, server)