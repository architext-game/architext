import tests.util as util

def test_use_exit():
    with util.Connection() as c:
        util.new_log_in(c)
        c.send("go door")
        assert "The Eyes Lab" in c.send("look")