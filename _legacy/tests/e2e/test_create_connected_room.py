import tests.util as util

def test_create_connected_room():
    with util.Connection() as c:
        # login with new user
        util.new_log_in(c)

        # create verb
        c.send("build")
        c.send("new_room")
        c.send("description")
        c.send("entrance name")
        c.send("exit name")

        c.send("go entrance")

        result = c.send("look")

        expected = (
"""new_room
─────────
description

⮕ Exits: exit name."""
)

        assert expected in result
        c.send("go exit")
        assert "The Legs Lab" in c.send("look")



