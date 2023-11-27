import tests.util as util

def test_connect_rooms():
    with util.Connection() as c:
        # login with new user
        util.new_log_in(c)

        c.send("link")
        c.send("2")
        c.send("road to 2")
        c.send("road to 1")
        assert "The Hands Lab" in c.send("go 2")
        c.send("go 1")
        assert "The Legs Lab" in c.send("look")