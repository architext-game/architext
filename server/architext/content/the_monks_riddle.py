THE_MONKS_RIDDLE = """{
    "original_name": "The Monk's Riddle",
    "original_description": "You see a poster explaining everything you need to know to play the Monk's Riddle.",
    "initial_room_id": "0",
    "rooms": [
        {
            "id": "0",
            "name": "The Monk's Riddle",
            "description": "You see a poster explaining everything you need to know to play the Monk's Riddle.",
            "exits": [
                {
                    "name": "a traslucent portal",
                    "description": "",
                    "destination_room_id": "1",
                    "visibility": "listed"
                }
            ],
            "items": [
                {
                    "name": "a poster",
                    "description": "The Monk's Riddle puts you and your friends in a seemingly abandoned monastery. You'll need to explore it, find clues and solve puzzles in order to discover what happened to its inhabitants.\\n\\nThe game lasts between 20-60 minutes. 2 to 4 players are recommended so consider bringing some friends with you. You can communicate using the say and shout verbs, or use a voice chat app like Discord. (You can join our official discord server here: https://discord.com/invite/CnQD9g3U5g )\\n\\nIn the monastery you'll JUST need to use these verbs:\\n  look <item> - to take a close look and find clues\\n  go <exit> - to travel between the different rooms\\n  exits - conveniently lists the obvious exits of the room\\n  items - lists the obvious items of the room\\n\\nWhen you enter a room first read its description. Then you can use the \\"look\\" verb to investigate all things you found there. When you have finished investigating, use the \\"go\\" verb to travel between rooms and keep exporing! You can use the \\"exits\\" and \\"items\\" verbs to see what you can interact with in the room if you get stuck.\\n\\nKeep in mind that there may be hidden item or exits, and these won't be listed by the \\"exits\\" or \\"items\\" verbs! Carefully reading item decriptions will allow you to find them.\\n\\nAlso, I recommend you to open a notepad so you can copy-paste cryptic clues that you may find. They may become meaningful later.\\n\\nNow go through the portal, and good luck!",
                    "visibility": "listed"
                }
            ]
        },
        {
            "id": "1",
            "name": "The Cloister",
            "description": "You are standing on a carpet of fresh grass in the inner courtyard of the monastery. The courtyard continues to the <north> and <east>.",
            "exits": [
                {
                    "name": "a traslucent portal",
                    "description": "",
                    "destination_room_id": "0",
                    "visibility": "listed"
                },
                {
                    "name": "north",
                    "description": "",
                    "destination_room_id": "2",
                    "visibility": "unlisted"
                },
                {
                    "name": "east",
                    "description": "",
                    "destination_room_id": "4",
                    "visibility": "unlisted"
                }
            ],
            "items": [
                {
                    "name": "a carpet of fresh grass",
                    "description": "You would gladly eat it if you were a cow.",
                    "visibility": "listed"
                }
            ]
        },
        {
            "id": "2",
            "name": "The Cloister",
            "description": "You are next to the walls of the monastery. They are built with large stones worn by the passage of time. In front of you is a door leading to a stairway. The courtyard continues to the south and to the east.",
            "exits": [
                {
                    "name": "south",
                    "description": "",
                    "destination_room_id": "1",
                    "visibility": "unlisted"
                },
                {
                    "name": "east",
                    "description": "",
                    "destination_room_id": "3",
                    "visibility": "unlisted"
                },
                {
                    "name": "a door leading to a stairway",
                    "description": "",
                    "destination_room_id": "5",
                    "visibility": "unlisted"
                }
            ],
            "items": [
                {
                    "name": "a carpet of fresh grass",
                    "description": "You would gladly eat it if you were a cow.",
                    "visibility": "listed"
                },
                {
                    "name": "the walls of the monastery",
                    "description": "",
                    "visibility": "listed"
                }
            ]
        },
        {
            "id": "3",
            "name": "The Cloister",
            "description": "You are standing in the northeast corner of the monastery courtyard. Next to a well grows fresh grass and some medicinal plants. The courtyard continues to the south and west.",
            "exits": [
                {
                    "name": "west",
                    "description": "",
                    "destination_room_id": "2",
                    "visibility": "unlisted"
                },
                {
                    "name": "south",
                    "description": "",
                    "destination_room_id": "4",
                    "visibility": "unlisted"
                },
                {
                    "name": "down the ladder",
                    "description": "",
                    "destination_room_id": "12",
                    "visibility": "hidden"
                }
            ],
            "items": [
                {
                    "name": "a carpet of fresh grass",
                    "description": "You would gladly eat it if you were a cow.",
                    "visibility": "listed"
                },
                {
                    "name": "some medicinal plants",
                    "description": "You are certain that the monks knew how to use them.",
                    "visibility": "listed"
                },
                {
                    "name": "a well",
                    "description": "The stone well is dry. At the bottom is the wooden bucket that used to carry the water, destroyed by the fall and the years. If you wanted to go down, it would be better to do it using the ladder on the side.",
                    "visibility": "listed"
                }
            ]
        },
        {
            "id": "4",
            "name": "The Cloister",
            "description": "In this area of the courtyard there is a large wooden door leading to the common rooms of the monastery. The courtyard continues to the north and west.",
            "exits": [
                {
                    "name": "west",
                    "description": "",
                    "destination_room_id": "1",
                    "visibility": "unlisted"
                },
                {
                    "name": "north",
                    "description": "",
                    "destination_room_id": "3",
                    "visibility": "unlisted"
                },
                {
                    "name": "a large wooden door",
                    "description": "",
                    "destination_room_id": "17",
                    "visibility": "unlisted"
                }
            ],
            "items": []
        },
        {
            "id": "5",
            "name": "A corridor between dormitories",
            "description": "After climbing the stairs you find a narrow corridor. There is hardly any light and the floorboards creak under your feet. There is a wooden door to your left and another one to your right. You can either return to the cloister by going down the stairs or keep moving towards the end of the corridor.",
            "exits": [
                {
                    "name": "down the stairs towards the cloister",
                    "description": "",
                    "destination_room_id": "2",
                    "visibility": "unlisted"
                },
                {
                    "name": "to the end of the corridor",
                    "description": "It has nothing special",
                    "destination_room_id": "6",
                    "visibility": "unlisted"
                },
                {
                    "name": "a wooden door to the right",
                    "description": "",
                    "destination_room_id": "7",
                    "visibility": "unlisted"
                },
                {
                    "name": "a wooden door to the left",
                    "description": "",
                    "destination_room_id": "8",
                    "visibility": "unlisted"
                }
            ],
            "items": []
        },
        {
            "id": "6",
            "name": "A corridor between dormitories",
            "description": "This is the end of the corridor. There are more room doors here, one on the left and one on the right. You can go back to the beginning of the corridor.",
            "exits": [
                {
                    "name": "back to the beginning of the corridor",
                    "description": "",
                    "destination_room_id": "5",
                    "visibility": "unlisted"
                },
                {
                    "name": "wooden door to the left",
                    "description": "",
                    "destination_room_id": "9",
                    "visibility": "unlisted"
                },
                {
                    "name": "a wooden door to the right",
                    "description": "",
                    "destination_room_id": "10",
                    "visibility": "unlisted"
                }
            ],
            "items": []
        },
        {
            "id": "7",
            "name": "A monk's quarters",
            "description": "The small bedroom has a musty smell. By the little light coming through the window you can see a messy bunk bed, a wooden chest, a table and a chair.  On the table is an envelope. A wooden door leads to the corridor.",
            "exits": [
                {
                    "name": "a wooden door back to the corridor",
                    "description": "",
                    "destination_room_id": "5",
                    "visibility": "unlisted"
                }
            ],
            "items": [
                {
                    "name": "the window",
                    "description": "A wooden casement window. One of the sashes is unhinged. Hardly any light enters through it.",
                    "visibility": "listed"
                },
                {
                    "name": "a messy bunk bed",
                    "description": "You wouldn't like to have to overnight here.",
                    "visibility": "listed"
                },
                {
                    "name": "a wooden chest",
                    "description": "Surely the monk kept his few belongings here. It is empty.",
                    "visibility": "listed"
                },
                {
                    "name": "a table",
                    "description": "The wood of the table is cracked. It has a hole for an inkwell. You can see an envelope resting on it.",
                    "visibility": "listed"
                },
                {
                    "name": "a chair",
                    "description": "It doesn't look very comfortable.",
                    "visibility": "listed"
                },
                {
                    "name": "an envelope",
                    "description": "It is an envelope with no return address, with a torn lacquer seal. It has a letter inside.",
                    "visibility": "listed"
                },
                {
                    "name": "a letter",
                    "description": "The ink has lost some of its color, but you are still able to make out part of the contents of the letter: \\"...disappeared ... hidden all these years ... answer to everything ... at the bottom of the well ... the real reason we are here\\". The letter has no signature.",
                    "visibility": "listed"
                }
            ]
        },
        {
            "id": "8",
            "name": "An empty room",
            "description": "You enter a small empty room. You can make out marks on the floor and walls, where there used to be furniture. But now there is only a small crucifix hanging on the wall. A wooden door leads back to the corridor.",
            "exits": [
                {
                    "name": "a wooden door back to the corridor",
                    "description": "",
                    "destination_room_id": "5",
                    "visibility": "unlisted"
                }
            ],
            "items": [
                {
                    "name": "a small crucifix",
                    "description": "It has an inscription: \\"O T T\\"",
                    "visibility": "listed"
                }
            ]
        },
        {
            "id": "9",
            "name": "A monk's bedroom",
            "description": "The small bedroom has a musty smell. With the little light coming through the window you can see a bunk bed with the thin mattress out of place, a wooden chest, a table and a chair. A wooden door leads to the corridor.",
            "exits": [
                {
                    "name": "a wooden door back to the corridor",
                    "description": "",
                    "destination_room_id": "6",
                    "visibility": "unlisted"
                }
            ],
            "items": [
                {
                    "name": "a wooden chest",
                    "description": "Surely the monk kept his few belongings here. It is empty.",
                    "visibility": "listed"
                },
                {
                    "name": "a chair",
                    "description": "It doesn't look very comfortable.",
                    "visibility": "listed"
                },
                {
                    "name": "a bunk bed with the thin mattress out of place",
                    "description": "It looks like the mattress was moved in a hurry. When you lift it up, you see a piece of paper hidden underneath.",
                    "visibility": "listed"
                },
                {
                    "name": "a piece of paper",
                    "description": "It looks like a note for the monk who slept here. Maybe he never read it. It says: \\"You say I am mad, that I commit sacrilege, but know that God has spoken to me. The answer to the second test, or at least a clue. It does have to do with our mantra \\"O T T\\", but that is not its meaning. It has none. It's what comes next. More letters. I've engraved them on the dining room table. But yet one is missing. I know the answer is the eighth... but I only saw up to the seventh. Does this all make sense to you?\\"",
                    "visibility": "listed"
                },
                {
                    "name": "a table",
                    "description": "The wood of the table is cracked. It has a hole for an inkwell.",
                    "visibility": "listed"
                }
            ]
        },
        {
            "id": "10",
            "name": "A monk's quarters",
            "description": "The small bedroom has a musty smell. With the little light coming through the window you can see a bunk bed, a decorated wooden chest, a table and a chair.  A wooden door leads back to the corridor.",
            "exits": [
                {
                    "name": "a wooden door back to the corridor",
                    "description": "",
                    "destination_room_id": "6",
                    "visibility": "unlisted"
                }
            ],
            "items": [
                {
                    "name": "a messy bunk bed",
                    "description": "You wouldn't like to have to overnight here.",
                    "visibility": "listed"
                },
                {
                    "name": "a table",
                    "description": "The wood of the table is cracked. It has a hole for an inkwell.",
                    "visibility": "listed"
                },
                {
                    "name": "a chair",
                    "description": "It doesn't look very comfortable.",
                    "visibility": "listed"
                },
                {
                    "name": "a decorated wooden chest",
                    "description": "It is a chest with a cross drawn on it. Inside is a small notebook.",
                    "visibility": "listed"
                },
                {
                    "name": "a small notebook",
                    "description": "This notebook seems to collect the monk's thoughts. The last sentences read as follows: \\"At last I found it. It is on shelf 28. I am waiting for God to speak to me, but I no longer hear him. I am going into the water, there I will meet him.\\"",
                    "visibility": "listed"
                }
            ]
        },
        {
            "id": "12",
            "name": "An underground cave",
            "description": "After crossing a narrow corridor at the bottom of the well you find a majestic room. The walls are completely smooth, and from a hole in the ceiling a single beam of light shines into the pool of subterranean water that dominates the chamber. You find an inscription everywhere you look, engraved on each surface. You can go up through the well, back to the cloister.",
            "exits": [
                {
                    "name": "up through the well stairs back to the cloister",
                    "description": "",
                    "destination_room_id": "3",
                    "visibility": "unlisted"
                },
                {
                    "name": "a pool of water",
                    "description": "You feel a mystic urge to go and step into the pool.",
                    "destination_room_id": "13",
                    "visibility": "unlisted"
                }
            ],
            "items": [
                {
                    "name": "an inscription",
                    "description": "The inscription reads: LETTERS, LIKE THE WORLD, ARE NOT THE WORK OF MEN, BUT OF THE LORD. DIVE INTO IT, BE BAPTIZED IN THE PSALM OF THE CHARACTERS. BLESSED IS HE WHO FINDS THE THREE CAPITAL LETTERS, FOR HIS SHALL BE THE EARTHLY AND DIVINE KNOWLEDGE.",
                    "visibility": "listed"
                }
            ]
        },
        {
            "id": "13",
            "name": "The Gibberish",
            "description": "Step by step you descend the steps leading to the pool. As you touch the water you notice something in you fading away. A current pulls you, and you notice how your body keeps going down the steps. Until the water reaches your waist. Until it reaches your neck. Until, in a fetal position, your whole body is submerged in the icy water, illuminated by the light coming through the ceiling of the cave. Until you don't breathe and everything fades away.\\n\\nSome time later, lines of violet light appear in front of you, and you find yourself standing naked. The lines dance and swirl around you, combining into recognizable shapes: capital letters, all of the alphabet. You feel them all calling to you, but only one of them is the right one. Which capital letter of the alphabet should you go to? What will happen to you if you choose the wrong one? It may be best not to take a chance without being sure. Maybe you still have time to wake up and get out of the water.",
            "exits": [
                {
                    "name": "wake up and get out of the water",
                    "description": "",
                    "destination_room_id": "12",
                    "visibility": "unlisted"
                },
                {
                    "name": "Q",
                    "description": "",
                    "destination_room_id": "14",
                    "visibility": "hidden"
                },
                {
                    "name": "A",
                    "description": "",
                    "destination_room_id": "36",
                    "visibility": "hidden"
                },
                {
                    "name": "B",
                    "description": "",
                    "destination_room_id": "36",
                    "visibility": "hidden"
                },
                {
                    "name": "C",
                    "description": "",
                    "destination_room_id": "30",
                    "visibility": "hidden"
                },
                {
                    "name": "D",
                    "description": "",
                    "destination_room_id": "33",
                    "visibility": "hidden"
                },
                {
                    "name": "E",
                    "description": "",
                    "destination_room_id": "36",
                    "visibility": "hidden"
                },
                {
                    "name": "F",
                    "description": "",
                    "destination_room_id": "33",
                    "visibility": "hidden"
                },
                {
                    "name": "G",
                    "description": "",
                    "destination_room_id": "36",
                    "visibility": "hidden"
                },
                {
                    "name": "H",
                    "description": "",
                    "destination_room_id": "38",
                    "visibility": "hidden"
                },
                {
                    "name": "I",
                    "description": "",
                    "destination_room_id": "36",
                    "visibility": "hidden"
                },
                {
                    "name": "J",
                    "description": "",
                    "destination_room_id": "30",
                    "visibility": "hidden"
                },
                {
                    "name": "K",
                    "description": "",
                    "destination_room_id": "34",
                    "visibility": "hidden"
                },
                {
                    "name": "L",
                    "description": "",
                    "destination_room_id": "34",
                    "visibility": "hidden"
                },
                {
                    "name": "M",
                    "description": "",
                    "destination_room_id": "30",
                    "visibility": "hidden"
                },
                {
                    "name": "N",
                    "description": "",
                    "destination_room_id": "37",
                    "visibility": "hidden"
                },
                {
                    "name": "O",
                    "description": "",
                    "destination_room_id": "33",
                    "visibility": "hidden"
                },
                {
                    "name": "P",
                    "description": "",
                    "destination_room_id": "36",
                    "visibility": "hidden"
                },
                {
                    "name": "R",
                    "description": "",
                    "destination_room_id": "30",
                    "visibility": "hidden"
                },
                {
                    "name": "S",
                    "description": "",
                    "destination_room_id": "33",
                    "visibility": "hidden"
                },
                {
                    "name": "T",
                    "description": "",
                    "destination_room_id": "34",
                    "visibility": "hidden"
                },
                {
                    "name": "U",
                    "description": "",
                    "destination_room_id": "38",
                    "visibility": "hidden"
                },
                {
                    "name": "V",
                    "description": "",
                    "destination_room_id": "36",
                    "visibility": "hidden"
                },
                {
                    "name": "W",
                    "description": "",
                    "destination_room_id": "30",
                    "visibility": "hidden"
                },
                {
                    "name": "X",
                    "description": "",
                    "destination_room_id": "33",
                    "visibility": "hidden"
                },
                {
                    "name": "Y",
                    "description": "",
                    "destination_room_id": "36",
                    "visibility": "hidden"
                },
                {
                    "name": "Z",
                    "description": "",
                    "destination_room_id": "30",
                    "visibility": "hidden"
                }
            ],
            "items": []
        },
        {
            "id": "14",
            "name": "The Gibberish",
            "description": "As you enter the Q it all makes sense, and you dive deeper, deeper, deeper, deeper into the Gibberish. What you didn't understand before seems simple now, but there is still so much you don't know. The letters are still around you. Inciting. Threatening. What's the next capital letter? If you don't know, maybe it's best to give up. Maybe your lungs haven't filled with water yet.",
            "exits": [
                {
                    "name": "E",
                    "description": "",
                    "destination_room_id": "15",
                    "visibility": "hidden"
                },
                {
                    "name": "wake up and get out of the water",
                    "description": "",
                    "destination_room_id": "12",
                    "visibility": "unlisted"
                },
                {
                    "name": "A",
                    "description": "",
                    "destination_room_id": "34",
                    "visibility": "hidden"
                },
                {
                    "name": "B",
                    "description": "",
                    "destination_room_id": "37",
                    "visibility": "hidden"
                },
                {
                    "name": "C",
                    "description": "",
                    "destination_room_id": "34",
                    "visibility": "hidden"
                },
                {
                    "name": "D",
                    "description": "",
                    "destination_room_id": "33",
                    "visibility": "hidden"
                },
                {
                    "name": "F",
                    "description": "",
                    "destination_room_id": "30",
                    "visibility": "hidden"
                },
                {
                    "name": "G",
                    "description": "",
                    "destination_room_id": "38",
                    "visibility": "hidden"
                },
                {
                    "name": "H",
                    "description": "",
                    "destination_room_id": "36",
                    "visibility": "hidden"
                },
                {
                    "name": "I",
                    "description": "",
                    "destination_room_id": "34",
                    "visibility": "hidden"
                },
                {
                    "name": "J",
                    "description": "",
                    "destination_room_id": "34",
                    "visibility": "hidden"
                },
                {
                    "name": "K",
                    "description": "",
                    "destination_room_id": "34",
                    "visibility": "hidden"
                },
                {
                    "name": "L",
                    "description": "",
                    "destination_room_id": "33",
                    "visibility": "hidden"
                },
                {
                    "name": "M",
                    "description": "",
                    "destination_room_id": "33",
                    "visibility": "hidden"
                },
                {
                    "name": "N",
                    "description": "",
                    "destination_room_id": "37",
                    "visibility": "hidden"
                },
                {
                    "name": "O",
                    "description": "",
                    "destination_room_id": "36",
                    "visibility": "hidden"
                },
                {
                    "name": "P",
                    "description": "",
                    "destination_room_id": "37",
                    "visibility": "hidden"
                },
                {
                    "name": "Q",
                    "description": "",
                    "destination_room_id": "38",
                    "visibility": "hidden"
                },
                {
                    "name": "R",
                    "description": "",
                    "destination_room_id": "37",
                    "visibility": "hidden"
                },
                {
                    "name": "S",
                    "description": "",
                    "destination_room_id": "30",
                    "visibility": "hidden"
                },
                {
                    "name": "T",
                    "description": "",
                    "destination_room_id": "30",
                    "visibility": "hidden"
                },
                {
                    "name": "U",
                    "description": "",
                    "destination_room_id": "38",
                    "visibility": "hidden"
                },
                {
                    "name": "V",
                    "description": "",
                    "destination_room_id": "37",
                    "visibility": "hidden"
                },
                {
                    "name": "W",
                    "description": "",
                    "destination_room_id": "30",
                    "visibility": "hidden"
                },
                {
                    "name": "X",
                    "description": "",
                    "destination_room_id": "37",
                    "visibility": "hidden"
                },
                {
                    "name": "Y",
                    "description": "",
                    "destination_room_id": "36",
                    "visibility": "hidden"
                },
                {
                    "name": "Z",
                    "description": "",
                    "destination_room_id": "38",
                    "visibility": "hidden"
                }
            ],
            "items": []
        },
        {
            "id": "15",
            "name": "The Gibberish",
            "description": "The O melts around you (or you around it?) and your consciousness rises. You know everything. The sciences are meaningless now. You feel yourself melting into the gibberish, deeper and deeper. But there is still the final test. There is still something that eludes you. A more basic Truth. A purer Truth. Something that seems unknowable. The capital letters dance around you, slower and slower, dizzyingly fast. Which is the last one? Which is it? If you don't know, maybe you can breathe one more time.",
            "exits": [
                {
                    "name": "S",
                    "description": "",
                    "destination_room_id": "16",
                    "visibility": "hidden"
                },
                {
                    "name": "wake up and get out of the water",
                    "description": "",
                    "destination_room_id": "12",
                    "visibility": "unlisted"
                },
                {
                    "name": "A",
                    "description": "",
                    "destination_room_id": "36",
                    "visibility": "hidden"
                },
                {
                    "name": "B",
                    "description": "",
                    "destination_room_id": "37",
                    "visibility": "hidden"
                },
                {
                    "name": "C",
                    "description": "",
                    "destination_room_id": "38",
                    "visibility": "hidden"
                },
                {
                    "name": "D",
                    "description": "",
                    "destination_room_id": "30",
                    "visibility": "hidden"
                },
                {
                    "name": "E",
                    "description": "",
                    "destination_room_id": "37",
                    "visibility": "hidden"
                },
                {
                    "name": "F",
                    "description": "",
                    "destination_room_id": "38",
                    "visibility": "hidden"
                },
                {
                    "name": "G",
                    "description": "",
                    "destination_room_id": "34",
                    "visibility": "hidden"
                },
                {
                    "name": "H",
                    "description": "",
                    "destination_room_id": "36",
                    "visibility": "hidden"
                },
                {
                    "name": "I",
                    "description": "",
                    "destination_room_id": "34",
                    "visibility": "hidden"
                },
                {
                    "name": "J",
                    "description": "",
                    "destination_room_id": "36",
                    "visibility": "hidden"
                },
                {
                    "name": "K",
                    "description": "",
                    "destination_room_id": "34",
                    "visibility": "hidden"
                },
                {
                    "name": "L",
                    "description": "",
                    "destination_room_id": "37",
                    "visibility": "hidden"
                },
                {
                    "name": "M",
                    "description": "",
                    "destination_room_id": "34",
                    "visibility": "hidden"
                },
                {
                    "name": "N",
                    "description": "",
                    "destination_room_id": "36",
                    "visibility": "hidden"
                },
                {
                    "name": "O",
                    "description": "",
                    "destination_room_id": "34",
                    "visibility": "hidden"
                },
                {
                    "name": "P",
                    "description": "",
                    "destination_room_id": "30",
                    "visibility": "hidden"
                },
                {
                    "name": "Q",
                    "description": "",
                    "destination_room_id": "36",
                    "visibility": "hidden"
                },
                {
                    "name": "R",
                    "description": "",
                    "destination_room_id": "37",
                    "visibility": "hidden"
                },
                {
                    "name": "T",
                    "description": "",
                    "destination_room_id": "34",
                    "visibility": "hidden"
                },
                {
                    "name": "U",
                    "description": "",
                    "destination_room_id": "37",
                    "visibility": "hidden"
                },
                {
                    "name": "V",
                    "description": "",
                    "destination_room_id": "38",
                    "visibility": "hidden"
                },
                {
                    "name": "W",
                    "description": "",
                    "destination_room_id": "36",
                    "visibility": "hidden"
                },
                {
                    "name": "X",
                    "description": "",
                    "destination_room_id": "37",
                    "visibility": "hidden"
                },
                {
                    "name": "Y",
                    "description": "",
                    "destination_room_id": "33",
                    "visibility": "hidden"
                },
                {
                    "name": "Z",
                    "description": "",
                    "destination_room_id": "36",
                    "visibility": "hidden"
                }
            ],
            "items": []
        },
        {
            "id": "16",
            "name": "The Gibberish",
            "description": "The S gets longer as you approach it. Its extremes get closer until they form an 8. An infinity in which you are immersed. In which you integrate. You dilute yourself... The ritual is complete. Now you can see them clearly, all the monks who were lost in the nothingness looking for omniscience. Their essences return your gaze as they lose themselves. You see the dormitories, the library, the chapel, the flowers in the courtyard.You see your inert body under the water of the cavern.  But you don't care anymore because you finally know everything. You know the same as one of the stones in the well, the same as the splintered wood of the monks' desks. You know that your journey ends here, the one that never began. In front of your Not-Self a point is born, which turns and grows. It accelerates and enlarges, until it becomes a hole. A portal. Your Not-Self is drawn into it, like water sucked into a sinkhole.",
            "exits": [
                {
                    "name": "the sinkhole portal",
                    "description": "",
                    "destination_room_id": "29",
                    "visibility": "listed"
                }
            ],
            "items": []
        },
        {
            "id": "17",
            "name": "The great hallway",
            "description": "An ominous corridor opens before you. The floor is polished, and marble columns support the vaulted ceiling. On one side you find a wooden door, on the other a large archway leading to another room. You can continue towards the end of the corridor. You can also return to the courtyard.",
            "exits": [
                {
                    "name": "back to the courtyard",
                    "description": "",
                    "destination_room_id": "4",
                    "visibility": "unlisted"
                },
                {
                    "name": "a wooden door",
                    "description": "",
                    "destination_room_id": "18",
                    "visibility": "unlisted"
                },
                {
                    "name": "a large archway",
                    "description": "",
                    "destination_room_id": "19",
                    "visibility": "unlisted"
                },
                {
                    "name": "continue to the end of the hallway",
                    "description": "",
                    "destination_room_id": "20",
                    "visibility": "unlisted"
                }
            ],
            "items": []
        },
        {
            "id": "18",
            "name": "The copyists' room",
            "description": "As you walk through the dooryou come to a dark room with only benches and desks. You wonder how the monks copied with so little light. There is an open book on one of the desks. A wooden door leads back to the hallway.",
            "exits": [
                {
                    "name": "a wooden door, back to the hallway",
                    "description": "",
                    "destination_room_id": "17",
                    "visibility": "unlisted"
                }
            ],
            "items": [
                {
                    "name": "some benches",
                    "description": "They do not look very comfortable.",
                    "visibility": "listed"
                },
                {
                    "name": "writing desks",
                    "description": "They are slanted copyist's desks, with a hole for the inkwell. They are made of wood, cracked by the pass of time.",
                    "visibility": "listed"
                },
                {
                    "name": "an open book",
                    "description": "It is a thick old book with sturdy covers. It seems that it will fall apart if you touch it. It is open, and in it you can read the following: \\"If in water you seek enlightenment, the first test requires good judgement: Eustaquio has what the great philosopher Maquiavelo had, but few other people do. For example, his friends Godfrey, Eulalia, Louis, Raphael and Mary do not have it. What is Eustaquio's precious treasure?\\".",
                    "visibility": "listed"
                }
            ]
        },
        {
            "id": "19",
            "name": "The great chapel",
            "description": "You arrive at a chapel lit by large windows. Carefully carved wooden chairs are arranged surrounding the altar. In the background, a large golden cross displays the inscription: \\"O T T\\".",
            "exits": [
                {
                    "name": "a large archway leading back to the hallway",
                    "description": "a large archway leading back to the hallway",
                    "destination_room_id": "17",
                    "visibility": "unlisted"
                }
            ],
            "items": [
                {
                    "name": "the large windows",
                    "description": "The large windows fill the room with a warm light.",
                    "visibility": "listed"
                },
                {
                    "name": "wooden chairs",
                    "description": "The chairs are carefully carved and well preserved. This is probably where the monks sat to chant and pray.",
                    "visibility": "listed"
                },
                {
                    "name": "a large golden cross",
                    "description": "The cross reads: \\"O T T\\".",
                    "visibility": "listed"
                }
            ]
        },
        {
            "id": "20",
            "name": "The great hallway",
            "description": "You are at the end of the hallway. At the ceiling, stained glass windows illuminate the room with an almost mystical light. On one side is a modest door, on the other, an ominous threshold. You can return to the beginning of the hallway.",
            "exits": [
                {
                    "name": "back to the beginning of the hallway",
                    "description": "",
                    "destination_room_id": "17",
                    "visibility": "unlisted"
                },
                {
                    "name": "a modest door",
                    "description": "",
                    "destination_room_id": "21",
                    "visibility": "unlisted"
                },
                {
                    "name": "an ominous threshold",
                    "description": "",
                    "destination_room_id": "24",
                    "visibility": "unlisted"
                }
            ],
            "items": [
                {
                    "name": "stained glass windows",
                    "description": "The colored glass draws an inscription: \\"O T T\\".",
                    "visibility": "listed"
                }
            ]
        },
        {
            "id": "21",
            "name": "The dining room",
            "description": "The humility of this room contrasts with the luxurious hallway. A long, coarse, cracked wooden table fills the room, surrounded by benches. A modest door leads back to the corridor. At the end of the room you can reach the kitchens.",
            "exits": [
                {
                    "name": "a modest door leading back to the hallway",
                    "description": "",
                    "destination_room_id": "20",
                    "visibility": "unlisted"
                },
                {
                    "name": "to the kitchens",
                    "description": "",
                    "destination_room_id": "22",
                    "visibility": "unlisted"
                }
            ],
            "items": [
                {
                    "name": "a large wooden table",
                    "description": "It is full of dry wine stains. As you run your hand over the table you notice a multitude of cracks... and you feel something strange that you can't see with the naked eye, some carved letters. It says \\"...F F S S\\". What does it mean?",
                    "visibility": "listed"
                }
            ]
        },
        {
            "id": "22",
            "name": "The kitchen",
            "description": "It is a modest kitchen with a few wood-burning stoves, an oven and a pantry.",
            "exits": [
                {
                    "name": "back to the dining room",
                    "description": "",
                    "destination_room_id": "21",
                    "visibility": "listed"
                }
            ],
            "items": [
                {
                    "name": "stoves",
                    "description": "They are worn out by the passage of time.",
                    "visibility": "listed"
                },
                {
                    "name": "an oven",
                    "description": "There's nothing inside.",
                    "visibility": "listed"
                },
                {
                    "name": "the pantry",
                    "description": "The pantry is empty, not even rats are left.",
                    "visibility": "listed"
                }
            ]
        },
        {
            "id": "24",
            "name": "The great library",
            "description": "Behind the ominous threshold is the great library of the monastery, the home of all the wisdom copied and translated by its inhabitants for generations. Shelves and shelves crammed with books occupy the room. In this section are shelves 1 to 10. You can go back through the threshold, or go deeper into the library.",
            "exits": [
                {
                    "name": "an ominous threshold leading back to the hallway",
                    "description": "",
                    "destination_room_id": "20",
                    "visibility": "unlisted"
                },
                {
                    "name": "deeper into the library",
                    "description": "",
                    "destination_room_id": "25",
                    "visibility": "unlisted"
                }
            ],
            "items": [
                {
                    "name": "shelf 1",
                    "description": "There's nothing special about that self",
                    "visibility": "listed"
                },
                {
                    "name": "shelf 2",
                    "description": "There's nothing special about that self",
                    "visibility": "listed"
                },
                {
                    "name": "shelf 3",
                    "description": "There's nothing special about that self",
                    "visibility": "listed"
                },
                {
                    "name": "shelf 4",
                    "description": "There's nothing special about that self",
                    "visibility": "listed"
                },
                {
                    "name": "shelf 5",
                    "description": "There's nothing special about that self",
                    "visibility": "listed"
                },
                {
                    "name": "shelf 6",
                    "description": "There's nothing special about that self",
                    "visibility": "listed"
                },
                {
                    "name": "shelf 7",
                    "description": "There's nothing special about that self",
                    "visibility": "listed"
                },
                {
                    "name": "shelf 8",
                    "description": "There's nothing special about that self",
                    "visibility": "listed"
                },
                {
                    "name": "shelf 9",
                    "description": "There's nothing special about that self",
                    "visibility": "listed"
                },
                {
                    "name": "shelf 10",
                    "description": "There's nothing special about that self",
                    "visibility": "listed"
                },
                {
                    "name": "books",
                    "description": "They seem like they would break apart if you touch them.",
                    "visibility": "listed"
                }
            ]
        },
        {
            "id": "25",
            "name": "The great library",
            "description": "The library continues. In this section you will find shelves 11 to 20. You can go back towards the entrance or go deeper into the library.",
            "exits": [
                {
                    "name": "back towards the entrance",
                    "description": "",
                    "destination_room_id": "24",
                    "visibility": "unlisted"
                },
                {
                    "name": "deeper into the library",
                    "description": "",
                    "destination_room_id": "26",
                    "visibility": "unlisted"
                }
            ],
            "items": [
                {
                    "name": "shelf 11",
                    "description": "There's nothing special about that self",
                    "visibility": "listed"
                },
                {
                    "name": "shelf 12",
                    "description": "There's nothing special about that self",
                    "visibility": "listed"
                },
                {
                    "name": "shelf 13",
                    "description": "There's nothing special about that self",
                    "visibility": "listed"
                },
                {
                    "name": "shelf 14",
                    "description": "There's nothing special about that self",
                    "visibility": "listed"
                },
                {
                    "name": "shelf 15",
                    "description": "There's nothing special about that self",
                    "visibility": "listed"
                },
                {
                    "name": "shelf 16",
                    "description": "There's nothing special about that self",
                    "visibility": "listed"
                },
                {
                    "name": "shelf 17",
                    "description": "There's nothing special about that self",
                    "visibility": "listed"
                },
                {
                    "name": "shelf 18",
                    "description": "There's nothing special about that self",
                    "visibility": "listed"
                },
                {
                    "name": "shelf 19",
                    "description": "There's nothing special about that self",
                    "visibility": "listed"
                },
                {
                    "name": "shelf 20",
                    "description": "There's nothing special about that self",
                    "visibility": "listed"
                }
            ]
        },
        {
            "id": "26",
            "name": "The great library",
            "description": "The library continues. In this section you will find shelves 21 to 30. You can go back towards the entrance or go deeper into the library.",
            "exits": [
                {
                    "name": "back towards the entrance",
                    "description": "",
                    "destination_room_id": "25",
                    "visibility": "unlisted"
                },
                {
                    "name": "deeper into the library",
                    "description": "",
                    "destination_room_id": "27",
                    "visibility": "unlisted"
                },
                {
                    "name": "a hidden corridor behind the shelf",
                    "description": "",
                    "destination_room_id": "28",
                    "visibility": "hidden"
                }
            ],
            "items": [
                {
                    "name": "shelf 21",
                    "description": "There's nothing special about that self",
                    "visibility": "listed"
                },
                {
                    "name": "shelf 22",
                    "description": "There's nothing special about that self",
                    "visibility": "listed"
                },
                {
                    "name": "shelf 23",
                    "description": "There's nothing special about that self",
                    "visibility": "listed"
                },
                {
                    "name": "shelf 24",
                    "description": "There's nothing special about that self",
                    "visibility": "listed"
                },
                {
                    "name": "shelf 25",
                    "description": "There's nothing special about that self",
                    "visibility": "listed"
                },
                {
                    "name": "shelf 26",
                    "description": "There's nothing special about that self",
                    "visibility": "listed"
                },
                {
                    "name": "shelf 27",
                    "description": "There's nothing special about that self",
                    "visibility": "listed"
                },
                {
                    "name": "shelf 28",
                    "description": "After a close examination of the shelf you spot a book that is strangely well conserved. You pull it and the shelf displaces to reveal a hidden corridor.",
                    "visibility": "listed"
                },
                {
                    "name": "shelf 29",
                    "description": "There's nothing special about that self",
                    "visibility": "listed"
                },
                {
                    "name": "shelf 30",
                    "description": "There's nothing special about that self",
                    "visibility": "listed"
                }
            ]
        },
        {
            "id": "27",
            "name": "The great library",
            "description": "This is the end of the library. In this section you will find shelves 31 to 40. You can go back towards the entrance of the library.",
            "exits": [
                {
                    "name": "back towards the entrance",
                    "description": "",
                    "destination_room_id": "26",
                    "visibility": "unlisted"
                }
            ],
            "items": [
                {
                    "name": "shelf 31",
                    "description": "There's nothing special about that self",
                    "visibility": "listed"
                },
                {
                    "name": "shelf 32",
                    "description": "There's nothing special about that self",
                    "visibility": "listed"
                },
                {
                    "name": "shelf 33",
                    "description": "There's nothing special about that self",
                    "visibility": "listed"
                },
                {
                    "name": "shelf 34",
                    "description": "There's nothing special about that self",
                    "visibility": "listed"
                },
                {
                    "name": "shelf 35",
                    "description": "There's nothing special about that self",
                    "visibility": "listed"
                },
                {
                    "name": "shelf 36",
                    "description": "There's nothing special about that self",
                    "visibility": "listed"
                },
                {
                    "name": "shelf 37",
                    "description": "There's nothing special about that self",
                    "visibility": "listed"
                },
                {
                    "name": "shelf 38",
                    "description": "There's nothing special about that self",
                    "visibility": "listed"
                },
                {
                    "name": "shelf 39",
                    "description": "There's nothing special about that self",
                    "visibility": "listed"
                },
                {
                    "name": "shelf 40",
                    "description": "There's nothing special about that self",
                    "visibility": "listed"
                }
            ]
        },
        {
            "id": "28",
            "name": "A hidden altar",
            "description": "Behind the secret entrance is a narrow cubic room with a lighted torch inside. In the center is an altar on which rests a stone slab. You can go back to the library.",
            "exits": [
                {
                    "name": "back to the library",
                    "description": "",
                    "destination_room_id": "26",
                    "visibility": "unlisted"
                }
            ],
            "items": [
                {
                    "name": "a lighted torch",
                    "description": "It doesn't seem the torch is going to go out any time soon.",
                    "visibility": "listed"
                },
                {
                    "name": "an altar",
                    "description": "There is a stone slab resting on it.",
                    "visibility": "listed"
                },
                {
                    "name": "a stone slab",
                    "description": "By the light of the torch, you can read written on the tablet: \\n\\nTo find absolute wisdom your search must be stopped. There are no more clues that can help you now. Listen deep inside yourself for a two-digit number whispered by the Lord. Subtract from the number the two digits that compose it. The letter that corresponds to the result is your answer to the final question.\\n\\n  99 -> n    98 -> r    97 -> a    96 -> f    95 -> f    94 -> r    93 -> z  92 -> f    91 -> u    90 -> y    89 -> b    88 -> s    87 -> v    86 -> j  85 -> k    84 -> e83 -> o    82 -> d    81 -> s    80 -> g    79 -> c  78 -> o    77 -> i    76 -> s    75 -> v    74 -> r    73 -> a    72 -> s  71 -> v    70 -> g    69 -> b    68 -> y    67 -> j    66 -> s    65 -> d  64 -> f    63 -> s    62 -> q    61 -> z    60 -> d    59 -> g    58 -> h  57 -> j    56 -> v    55 -> t    54 -> s    53 -> e    52 -> a    51 -> f  50 -> r    49 -> v    48 -> d    47 -> q    46 -> z    45 -> s    44 -> f  43 -> e    42 -> i    41 -> y    40 -> n    39 -> v    38 -> n    37 -> f  36 -> s    35 -> n    34 -> a    33 -> q    32 -> s    31 -> c    30 -> g  29 -> j    28 -> v    27 -> s    26 -> b    25 -> n    24 -> m    23 -> z  22 -> x    21 -> c    20 -> w    19 -> y    18 -> s    17 -> h    16 -> f  15 -> l    14 -> ñ    13 -> j    12 -> b    11 -> c    10 -> r    9 -> s   8  -> w    7  -> h    6  -> i    5  -> u    4  -> t    3  -> s    2 -> b      1 -> c     0  -> s",
                    "visibility": "listed"
                }
            ]
        },
        {
            "id": "29",
            "name": "The end",
            "description": "Congratulations! You did it! I hope you liked it -)\\n\\nNow you have a little example of what can be built by an Architext like you. The Monk's Riddle was created using only what you'll find if you type: \\"help building\\".\\n\\nConsider joining our discord server, where we can chat about Architext!\\nhttps://discord.com/invite/CnQD9g3U5g\\n\\nThank you for playing.\\n\\nOliver",
            "exits": [
                {
                    "name": "back to the beginning",
                    "description": "",
                    "destination_room_id": "0",
                    "visibility": "listed"
                }
            ],
            "items": []
        },
        {
            "id": "30",
            "name": "A maze of mistakes",
            "description": "This place is made of the anguish of those that lost their way in the Gibberish. If you are lucky maybe you can find your way out of here.",
            "exits": [
                {
                    "name": "a way back",
                    "description": "",
                    "destination_room_id": "33",
                    "visibility": "listed"
                },
                {
                    "name": "a way forth",
                    "description": "",
                    "destination_room_id": "34",
                    "visibility": "listed"
                }
            ],
            "items": []
        },
        {
            "id": "33",
            "name": "A maze of mistakes",
            "description": "This place is made of the anguish of those that lost their way in the Gibberish. If you are lucky maybe you can find your way out of here.",
            "exits": [
                {
                    "name": "a way forth",
                    "description": "",
                    "destination_room_id": "30",
                    "visibility": "listed"
                },
                {
                    "name": "away back",
                    "description": "",
                    "destination_room_id": "33",
                    "visibility": "listed"
                }
            ],
            "items": []
        },
        {
            "id": "34",
            "name": "A maze of mistakes",
            "description": "This place is made of the anguish of those that lost their way in the Gibberish. If you are lucky maybe you can find your way out of here.",
            "exits": [
                {
                    "name": "a way back",
                    "description": "",
                    "destination_room_id": "30",
                    "visibility": "listed"
                },
                {
                    "name": "go forth",
                    "description": "",
                    "destination_room_id": "35",
                    "visibility": "listed"
                }
            ],
            "items": []
        },
        {
            "id": "35",
            "name": "A light in the darkness",
            "description": "You feel lucidity coming back too your mind. You wake up with an intense urge to breathe.",
            "exits": [
                {
                    "name": "out of the water",
                    "description": "",
                    "destination_room_id": "12",
                    "visibility": "listed"
                }
            ],
            "items": []
        },
        {
            "id": "36",
            "name": "A maze of mistakes",
            "description": "This place is made of the anguish of those that lost their way in the Gibberish. If you are lucky maybe you can find your way out of here.",
            "exits": [
                {
                    "name": "a way back",
                    "description": "",
                    "destination_room_id": "35",
                    "visibility": "listed"
                },
                {
                    "name": "a way forth",
                    "description": "",
                    "destination_room_id": "37",
                    "visibility": "listed"
                }
            ],
            "items": []
        },
        {
            "id": "37",
            "name": "A maze of mistakes",
            "description": "This place is made of the anguish of those that lost their way in the Gibberish. If you are lucky maybe you can find your way out of here.",
            "exits": [
                {
                    "name": "a way back",
                    "description": "",
                    "destination_room_id": "36",
                    "visibility": "listed"
                },
                {
                    "name": "a way forth",
                    "description": "",
                    "destination_room_id": "38",
                    "visibility": "listed"
                }
            ],
            "items": []
        },
        {
            "id": "38",
            "name": "A maze of mistakes",
            "description": "This place is made of the anguish of those that lost their way in the Gibberish. If you are lucky maybe you can find your way out of here.",
            "exits": [
                {
                    "name": "a way back",
                    "description": "",
                    "destination_room_id": "37",
                    "visibility": "listed"
                },
                {
                    "name": "a way forth",
                    "description": "",
                    "destination_room_id": "38",
                    "visibility": "listed"
                }
            ],
            "items": []
        }
    ]
}"""


THE_MONKS_RIDDLE_ENCODED = """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"""