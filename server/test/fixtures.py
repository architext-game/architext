from architext.core.adapters.fake_uow import FakeUnitOfWork
from architext.core.domain.entities.exit import Exit
from architext.core.domain.entities.user import User
from architext.core.domain.entities.world import World
from architext.core.domain.entities.world_template import WorldTemplate
from architext.core.domain.entities.room import Room
from architext.core import Architext

def createTestData() -> Architext:
    emptytemplate = WorldTemplate(
        id="emptytemplate",
        name="New World",
        description="An Empty World",
        author_id=None,
        world_encoded_json="""eJx9kcFOwzAMhl/F9MKl4gG4TRxB4jCkCaFpilp3tZbEVZxOG9Penbi0tIPSS6LE9v/5ty8ZB9qTN3bnjcPsEbLXNmKADdlSshzGeIlSBGoisde0F4z3AnhqLAeEWCO0no4YBO+0jDxFSlWB2e2o1ApWYX1rXG9Jvx+XbCY69LJuTIH68Qv+zi2YhK0sm0h+D+S7Fo5GokcR4OqmpRyMZY8PKoUnij15wLxxly1Kk5qaGeKmNhEMeCoQVKFPSXCjKVOfo8x1e81hMHijPpBX8MSfZ1gvkFdQ/EmZ9/BMsajRz2p0jYtDa5OcQ4EqsFPXAResHHrFzsaE9N9e+kEWbMvvA10Tz7qRBci4+Zt5HUY3A3nJoOMSg4dJ1c+Qtkn3C67G+X8=""",
        visibility="public"
    )
    templateforme = WorldTemplate(
        id="templateforme",
        name="A template only for me",
        description="For the new worlds I create",
        author_id="oliver",
        world_encoded_json="""eJx9kcFOwzAMhl/F9MKl4gG4TRxB4jCkCaFpilp3tZbEVZxOG9Penbi0tIPSS6LE9v/5ty8ZB9qTN3bnjcPsEbLXNmKADdlSshzGeIlSBGoisde0F4z3AnhqLAeEWCO0no4YBO+0jDxFSlWB2e2o1ApWYX1rXG9Jvx+XbCY69LJuTIH68Qv+zi2YhK0sm0h+D+S7Fo5GokcR4OqmpRyMZY8PKoUnij15wLxxly1Kk5qaGeKmNhEMeCoQVKFPSXCjKVOfo8x1e81hMHijPpBX8MSfZ1gvkFdQ/EmZ9/BMsajRz2p0jYtDa5OcQ4EqsFPXAResHHrFzsaE9N9e+kEWbMvvA10Tz7qRBci4+Zt5HUY3A3nJoOMSg4dJ1c+Qtkn3C67G+X8=""",
        visibility="private"
    )
    braggingtemplate = WorldTemplate(
        id="braggingtemplate",
        name="A template everyone should see",
        description="To brag about",
        author_id="oliver",
        world_encoded_json="""eJx9kcFOwzAMhl/F9MKl4gG4TRxB4jCkCaFpilp3tZbEVZxOG9Penbi0tIPSS6LE9v/5ty8ZB9qTN3bnjcPsEbLXNmKADdlSshzGeIlSBGoisde0F4z3AnhqLAeEWCO0no4YBO+0jDxFSlWB2e2o1ApWYX1rXG9Jvx+XbCY69LJuTIH68Qv+zi2YhK0sm0h+D+S7Fo5GokcR4OqmpRyMZY8PKoUnij15wLxxly1Kk5qaGeKmNhEMeCoQVKFPSXCjKVOfo8x1e81hMHijPpBX8MSfZ1gvkFdQ/EmZ9/BMsajRz2p0jYtDa5OcQ4EqsFPXAResHHrFzsaE9N9e+kEWbMvvA10Tz7qRBci4+Zt5HUY3A3nJoOMSg4dJ1c+Qtkn3C67G+X8=""",
        visibility="public"
    )
    rabbittemplate = WorldTemplate(
        id="rabbittemplate",
        name="Misterious Template",
        description="This is so misterious",
        author_id="rabbit",
        world_encoded_json="""eJx9kcFOwzAMhl/F9MKl4gG4TRxB4jCkCaFpilp3tZbEVZxOG9Penbi0tIPSS6LE9v/5ty8ZB9qTN3bnjcPsEbLXNmKADdlSshzGeIlSBGoisde0F4z3AnhqLAeEWCO0no4YBO+0jDxFSlWB2e2o1ApWYX1rXG9Jvx+XbCY69LJuTIH68Qv+zi2YhK0sm0h+D+S7Fo5GokcR4OqmpRyMZY8PKoUnij15wLxxly1Kk5qaGeKmNhEMeCoQVKFPSXCjKVOfo8x1e81hMHijPpBX8MSfZ1gvkFdQ/EmZ9/BMsajRz2p0jYtDa5OcQ4EqsFPXAResHHrFzsaE9N9e+kEWbMvvA10Tz7qRBci4+Zt5HUY3A3nJoOMSg4dJ1c+Qtkn3C67G+X8=""",
        visibility="private"
    )

    rabbithole_world = World(
        id="rabbithole",
        name="Down The Rabbit Hole",
        description="A magical place.",
        initial_room_id="rabbitholeroom",
        owner_user_id="rabbit"
    )
    rabbithole_room = Room(
        id="rabbitholeroom",
        name="A really big room",
        description="It seems you drank something that made you small.",
        world_id="rabbithole"
    )

    public_tabern = World(
        id="tabern",
        name="Public tabern",
        description="A public tabern",
        initial_room_id="tabern_table",
        owner_user_id=None,
        visibility="public"
    )
    a_table_in_the_tabern = Room(
        id="tabern_table",
        name="A table in the tabern",
        description="It is somewhat dirty",
        world_id="tabern"
    )

    outer_world = World(
        id="outer",
        name="Outer Wilds",
        description="Let's explore the universe!",
        initial_room_id="space",
        owner_user_id="oliver",
        visibility="public"
    )
    space = Room(
        id="space",
        name="Space",
        description="You are floating in the vastness of the universe, alone.",
        world_id="outer",
        exits=[
            Exit(name="To the spaceship", destination_room_id="spaceship", description="What a nice exit")
        ],
    )
    spaceship = Room(
        id="spaceship",
        name="A Cozy Spaceship",
        description="A cozy Spaceship",
        exits=[
            Exit(name="To Oliver's Room", destination_room_id="olivers", description="A nice smell comes from there"),
            Exit(name="To Alice's Room", destination_room_id="alices", description="A nice smell comes from there"),
            Exit(name="To Bob's Room", destination_room_id="bobs", description="A nice smell comes from there"),
            Exit(name="To Space", destination_room_id="outerroom", description="To the cold cold emptyness"),
        ],
        world_id="outer"
    )
    olivers = Room(
        id="olivers",
        name="Oliver's Room",
        description="This is Oliver's Room. The is an Auto door to bathroom.",
        exits=[
            Exit(name="To the spaceship", destination_room_id="spaceship", description="What a nice exit"),
            Exit(name="To Alice's Room", destination_room_id="alices", description="A nice smell comes from there"),
            Exit(name="To Bob's Room", destination_room_id="bobs", description="A nice smell comes from there"),
            Exit(name="Visible door to bathroom", destination_room_id="oliversbathroom", description="A bad smell comes from there", visibility="visible"),
            Exit(name="Auto door to bathroom", destination_room_id="oliversbathroom", description="A bad smell comes from there", visibility="auto"),
            Exit(name="Secret exit", destination_room_id="space", description="My secret scape pod", visibility="hidden"),
        ],
        world_id="outer"
    )
    private_bathroom = Room(
        id="oliversbathroom",
        name="The Oliver's room private bathroom",
        description="How lucky is it that Oliver has a bathroom in his room!",
        exits=[
            Exit(name="To Oliver's Room", destination_room_id="olivers", description="A nice smell comes from there"),
        ],
        world_id="outer"
    )
    alices = Room(
        id="alices",
        name="Alice's Room",
        description="This is Alice's Room",
        exits=[
            Exit(name="To the spaceship", destination_room_id="spaceship", description="What a nice exit"),
            Exit(name="To Oliver's Room", destination_room_id="olivers", description="A nice smell comes from there"),
            Exit(name="To Bob's Room", destination_room_id="bobs", description="A nice smell comes from there"),
        ],
        world_id="outer"
    )
    bobs = Room(
        id="bobs",
        name="Bob's Room",
        description="This is Bob's Room",
        exits=[
            Exit(name="To the spaceship", destination_room_id="spaceship", description="What a nice exit"),
            Exit(name="To Oliver's Room", destination_room_id="olivers", description="A nice smell comes from there"),
            Exit(name="To Alice's Room", destination_room_id="alices", description="A nice smell comes from there"),
        ],
        world_id="outer"
    )

    oliver_place = World(
        id="oliver_place",
        name="The private oliver's world",
        description="Only Oliver comes here",
        initial_room_id="solitude",
        owner_user_id="oliver",
        visibility="public"
    )
    solitude = Room(
        id="solitude",
        name="Solitude",
        description="Where only one person fits",
        world_id="oliver_place"
    )

    easteregg_world = World(
        id="easteregg",
        name="Easter Egg",
        description="Only the best find this world",
        initial_room_id="easteregg_room",
        owner_user_id=None
    )
    easteregg_room = Room(
        id="easteregg_room",
        name="CONGRATS!",
        description="You found the easter egg :D",
        world_id="easteregg"
    )

    oliver = User(
        id="oliver",
        name="Oliver",
        email="oliver@example.com",
        room_id="olivers",
        password_hash=b"asdasd",
        visited_world_ids={easteregg_world.id}
    )
    alice = User(
        id="alice",
        name="Alice",
        email="alice@example.com",
        room_id="alices",
        password_hash=b"asdasd"
    )
    bob = User(
        id="bob",
        name="Bob",
        email="bob@example.com",
        room_id="bobs",
        password_hash=b"asdasd"
    )
    charlie = User(
        id="charlie",
        name="Charlie",
        email="charlie@example.com",
        room_id=None,
        password_hash=b"asdasd"
    )
    dave = User(
        id="dave",
        name="Dave",
        email="dave@example.com",
        room_id="bobs",
        password_hash=b"asdasd"
    )
    rabbit = User(
        id="rabbit",
        name="Rabbit",
        email="rabbit@example.com",
        room_id="rabbitholeroom",
        password_hash=b"asdasd"
    )
    uow = FakeUnitOfWork()
    uow.world_templates.save_world_template(emptytemplate)
    uow.world_templates.save_world_template(templateforme)
    uow.world_templates.save_world_template(braggingtemplate)
    uow.world_templates.save_world_template(rabbittemplate)
    uow.worlds.save_world(rabbithole_world)
    uow.worlds.save_world(outer_world)
    uow.worlds.save_world(public_tabern)
    uow.worlds.save_world(oliver_place)
    uow.worlds.save_world(easteregg_world)
    uow.rooms.save_room(rabbithole_room)
    uow.rooms.save_room(space)
    uow.rooms.save_room(spaceship)
    uow.rooms.save_room(olivers)
    uow.rooms.save_room(private_bathroom)
    uow.rooms.save_room(alices)
    uow.rooms.save_room(bobs)
    uow.rooms.save_room(a_table_in_the_tabern)
    uow.rooms.save_room(solitude)
    uow.rooms.save_room(easteregg_room)
    uow.users.save_user(oliver)
    uow.users.save_user(alice)
    uow.users.save_user(bob)
    uow.users.save_user(charlie)
    uow.users.save_user(dave)
    uow.users.save_user(rabbit)
    return Architext(uow)