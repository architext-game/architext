import tests.util as util

def test_delete_room():
    with util.Connection() as c:
        # login with new user
        util.new_log_in(c)
        assert "The Hands Lab" in c.send("tp 2")
        c.send("look")
        assert "The room and the exits leading to it have been deleted." in c.send("deleteroom")
        assert "The Legs Lab" in c.send("look")


def test_delete_exit():
    with util.Connection() as c:
        util.new_log_in(c)
        assert "Exits: a white metal door" in c.send("look")
        assert 'Exit "a white metal door" has been deleted' in c.send("deleteexit a white metal door")
        assert "Exits: a white metal door" not in c.send('look')


def test_delete_item():
    with util.Connection() as c:
        util.new_log_in(c)

        c.send("tp 3")
        assert "You see a poster" in c.send("look")
        assert 'Item "a poster" has been deleted' in c.send("deleteitem a poster")
        assert "👁 You see a poster." not in c.send("look")
