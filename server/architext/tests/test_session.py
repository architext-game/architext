from architext.adapters.repository import FakeRepository
from architext.session import Session
from architext.adapters.sender import FakeSender

def signup(session: Session, name='oliver'):
    session.process_message('oliver')
    session.process_message('password')
    session.process_message('password')
    session.process_message('email@email.com')

def test_signup():
    sender = FakeSender()
    repository = FakeRepository()
    session = Session(repository=repository, sender=sender)
    signup(session)
    for m in sender._sent:
        print(m[0])
        print(m[1])
    assert 'You are in First World' in sender._sent[-1][1]

def test_look():
    sender = FakeSender()
    repository = FakeRepository()
    session = Session(repository=repository, sender=sender)
    signup(session)
    for m in sender._sent:
        print(m[0])
        print(m[1])
    session.process_message('look')
    assert 'First Room' in sender._sent[-1][1]

def test_build():
    sender = FakeSender()
    repository = FakeRepository()
    session = Session(repository=repository, sender=sender)
    signup(session)
    session.process_message('build')
    session.process_message('My Room')
    session.process_message('Whaaaa, cool rooom')
    session.process_message('door')
    session.process_message('exit')
    session.process_message('look')
    session.process_message('go door')
    assert 'Whaaaa, cool rooom' in sender._sent[-1][1]
    session.process_message('go exit')
    assert 'First Room' in sender._sent[-1][1]

    for m in sender._sent:
        print(m[0])
        print(m[1])
