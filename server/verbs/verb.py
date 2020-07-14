class Verb():
    command = 'verb '

    @classmethod
    def can_process(cls, message):
        if message.startswith(cls.command):
            return True
        else:
            return False

    def __init__(self, session):
        self.session = session
        self.finished = False

    def process(self, message):
        raise Exception('Abstract method of interface Verb not implemented')

    def command_finished(self):
        return self.finished