import tests.util as util

def test_create_item():
    with util.Connection() as c:
        # login with new user
        util.new_log_in(c)
        c.send("craft")
        c.send("Potato")
        c.send("It is a really good potato")
        c.send("takable")
        assert "It is a really good potato" in c.send("look potato")


def test_create_saved_item():
    with util.Connection() as c:
        # login with new user
        util.new_log_in(c)
        c.send("craftsaved")
        c.send("Potato")
        c.send("It is a really good potato")
        c.send("listed")
        assert "You can't find that here." in c.send("look potato")
        c.send("spawn Potato#1")
        assert "It is a really good potato" in c.send("look potato")