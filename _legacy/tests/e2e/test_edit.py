import tests.util as util

def test_edit_item():
    with util.Connection() as c:
        util.new_log_in(c)

        c.send("tp 3")
        assert "You see a poster" in c.send("look")
        c.send("edit a poster")
        c.send("0")
        c.send("a big poster")
        assert "👁 You see a big poster." in c.send("look") 

# EPIC BUG
# def test_edit_exit():
#     with util.Connection() as c:
#         util.new_log_in(c)
#         c.send("tp 3")
#         assert "Exits: a ceiling trapdoor" in c.send("look")
#         c.send("edit a ceiling trapdoor")
#         c.send("0")
#         c.send("a floor trapdoor")
#         assert "⮕ Exits: a floor trapdoor" in c.send("look") 
#         c.send('edit a floor trapdoor')
#         c.send('3')
#         c.send('0')
#         c.send('go trapdoor')
#         assert 'The Legs Lab' in c.send('look')


def test_edit_world():
    with util.Connection() as c:
        util.new_log_in(c)
        world_info = c.send('worldinfo')
        assert 'Name: The Museum of Architexture' in world_info
        assert 'Free edition: False' in world_info
        assert 'This world is private' in world_info
        c.send("editworld")
        c.send('0')
        c.send('patataworld')
        assert 'Name: patataworld' in c.send('worldinfo')
        c.send("editworld")
        c.send('1')
        c.send('yes')
        assert 'This world is public' in c.send('worldinfo')
        c.send("editworld")
        c.send('2')
        c.send('0')
        assert 'Free edition: True' in c.send('worldinfo')
