import tests.util as util

def test_add_verb_to_world():
    with util.Connection() as c:
        # login with new user
        util.new_log_in(c)

        # create verb
        c.send("verb world")
        c.send("verbname")
        c.send("textroom the verb executed")
        c.send("OK")

        # use verb
        data = c.send("verbname")

        assert util.check_end(data, 'the verb executed')

def test_add_verb_to_room():
    with util.Connection() as c:
        util.new_log_in(c)

        # create verb
        c.send("verb room")
        c.send("verbname")
        c.send("textroom the verb executed")
        c.send("OK")

        # use verb
        data = c.send("verbname")

        assert util.check_end(data, 'the verb executed')

def test_add_verb_to_item():
    with util.Connection() as c:
        util.new_log_in(c)

        # create item
        c.send("craft")
        c.send("patata")
        c.send("una patata hermosa")
        c.send("listed")

        # create verb
        c.send("verb patata")
        c.send("verbname")
        c.send("textroom the verb executed")
        c.send("OK")

        # use verb
        data = c.send("verbname patata")

        assert util.check_end(data, 'the verb executed')