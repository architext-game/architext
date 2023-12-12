import socketio
from architext.session import Session
from architext.adapters.repository import FakeRepository
from architext.adapters.sender import SocketIOSender
import typing

# Create a Socket.IO server
sio = socketio.Server()

repository = FakeRepository()

sessions: typing.Dict[str, Session] = {}
userid_to_sid: typing.Dict[str, str] = {}

def get_sid(user_id):
    return userid_to_sid[user_id]

@sio.event
def connect(sid, environ):
    sender = SocketIOSender(repository=repository, sio=sio, socket_id=sid)
    sessions[sid] = Session(repository=repository, sender=sender, connection_id=sid)
    print("connect ", sid)

@sio.event
def message(sid, data):
    sessions[sid].process_message(data)
    print("message", data, "sid", sid)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

# Run the server
if __name__ == '__main__':
    # Create a simple server application
    app = socketio.WSGIApp(sio)

    # Use eventlet or gevent for asynchronous server
    import eventlet
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
