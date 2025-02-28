from architext.core.queries.world_to_text import encode_text


EMPTY_WORLD = """{
  "original_name": "Imported",
  "original_description": "Tutorial",
  "initial_room_id": "8291ea5c-8c07-4b21-9b7f-67e3954ed3bc",
  "rooms": [
    {
      "id": "8291ea5c-8c07-4b21-9b7f-67e3954ed3bc",
      "name": "A New World",
      "description": "Type \\"look poster\\" for a brief refresher on architexture. You can use \\"remodel\\" to edit this room. Don't forget to rename your world from \\"Edit World Details\\" in the top left menu.",
      "exits": [],
      "items": [
        {
          "name": "the Advanced Architexture Manual",
          "description": "Manual on all the things that normal people can do:\\n\\n- \\"look\\" to look at their surroundings.\\n- \\"look [item/exit]\\" to examine something in detail.\\n- \\"go [exit]\\" to use an exit.\\n- \\"items\\" to get a list of all obvious items in the room.\\n- \\"exits\\" to get a list of all obvious exits in the room.\\n\\nManual on all things that an architext can do:\\n\\n- \\"craft\\" to create a new object.\\n- \\"build\\" to add a new room.\\n- \\"edit [item/exit]\\" to modify an object or an exit.\\n- \\"delete [item/exit]\\" to remove something permanently. ⚠ No undo!\\n- \\"info\\" to view details of your current room.\\n- \\"link\\" to connect two rooms with an exit.\\n- \\"remodel\\" to edit your current room.\\n- \\"raze\\" to delete your room and everything inside. 🚨 No turning back!\\n\\n⚠ You can only use architext commands in a world you own.",
          "visibility": "listed"
        },
        {
          "name": "a huge poster displaying a brief intro on architecture",
          "description": "The poster reads:\\n\\n🔨 Architext, welcome to your workshop! 🎉\\n\\nHere, you are like a god—you can bring your imagination to life. ✨ You can type:\\n\\n🛠 \\"craft\\" to create a new object.\\n🏗 \\"build\\" to build a new room.\\n\\n💡 Try them now, and tell your family and friends that you’re a true Architext! 🏗✨\\n\\n⚠ You can only use these commands in a world you own. No messing around in other people's worlds! 🚫\\n\\nLook at the Advanced Architexture Manual for more advanced creation tools.",
          "visibility": "auto"
        }
      ]
    }
  ]
}"""

EMPTY_WORLD_ENCODED = encode_text(EMPTY_WORLD)