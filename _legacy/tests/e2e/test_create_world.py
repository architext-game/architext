import tests.util as util

def test_create_world():
    with util.Connection() as c:
        util.new_log_in(c)
        c.send("exitworld")
        c.send("+")
        c.send("patatamundo")
        assert 'You are in patatamundo' in c.send("asd")

