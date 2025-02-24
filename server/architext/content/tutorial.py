TUTORIAL = """{
    "original_name": "The Legs Lab",
    "original_description": "You awake in a white room. A robotic voice says:\\n\\nWelcome, Architext. My purpose is to awake your virtual limbs and senses. Please listen carefully. Now type \\"go door\\" to use your legs.",
    "initial_room_id": "0",
    "rooms": [
        {
            "id": "0",
            "name": "The Legs Lab",
            "description": "You awake in a white room. A robotic voice says:\\n\\nWelcome, Architext. My purpose is to awake your virtual limbs and senses. Please listen carefully. Now type \\"go door\\" to use your legs.",
            "exits": [
                {
                    "name": "a white metal door",
                    "description": "",
                    "destination_room_id": "1",
                    "visibility": "listed"
                }
            ],
            "items": []
        },
        {
            "id": "1",
            "name": "The Eyes Lab",
            "description": "You crossed the door into another cubic room. The wall in front of you is covered by a huge curtain. \\n\\nGood job. In Architext you usually act by writing a verb followed by an object, like you did by writing \\"go door\\". \\"go\\" is the verb, and \\"door\\" is the object.\\n\\nIn Architext you can also \\"look\\". If your virtual eyes work, look at the curtain  ─ the voice says",
            "exits": [
                {
                    "name": "back to the Legs Lab",
                    "description": "",
                    "destination_room_id": "0",
                    "visibility": "unlisted"
                },
                {
                    "name": "a hidden corridor",
                    "description": "",
                    "destination_room_id": "2",
                    "visibility": "hidden"
                }
            ],
            "items": [
                {
                    "name": "a big white curtain",
                    "description": "You get a closer look at the curtain and find that there is a secret corridor hidden behind it! Maybe you can go through it with \\"go corridor\\"?",
                    "visibility": "listed"
                }
            ]
        },
        {
            "id": "2",
            "name": "The Hands Lab",
            "description": "Congrats! Lets see if you can exit this final room. I recommend you to look at every item you find, looking for clues. You can also just type \\"look\\" without an object to look at the room again.\\n\\nAn old oriental carpet covers the aseptic floor of the lab room. Oddly enough, there is a small mailbox next to it. They clearly don't belong here.\\n\\nThere is a poster with tips that may help you escape. Write \\"look poster\\" ONLY if you need to.",
            "exits": [
                {
                    "name": "back to the Eyes Lab",
                    "description": "",
                    "destination_room_id": "1",
                    "visibility": "unlisted"
                },
                {
                    "name": "a trapdoor",
                    "description": "",
                    "destination_room_id": "3",
                    "visibility": "hidden"
                }
            ],
            "items": [
                {
                    "name": "a small mailbox",
                    "description": "It appears to be something inside, but the mailbox is closed! Maybe try \\"open mailbox\\"?",
                    "visibility": "listed"
                },
                {
                    "name": "an old carpet",
                    "description": "It is worn out and grubby. In fact, you have the impression that the carpet has been dragged out of place many, many times.",
                    "visibility": "listed"
                },
                {
                    "name": "a poster",
                    "description": "READ JUST WHAT YOU NEED!\\n\\nUse the \\"look <item>\\" verb to look at items in the room (the mailbox, for example).\\n\\nCarefully read the item's description. They'll tell you what to do.\\n\\nIf you find a leaflet, also look at it!\\n\\nYou have to do something with the carpet other than looking at it. (Tip: it is a new verb that you haven't used before. Look at the carpet for clues!)\\n\\nYou may need to have taken a key in order to open an exit (\\"open\\" and \\"take\\" are also verbs you can use).\\n\\nIf you are really stuck and want to see exacly what you need to do, write \\"look solution\\".",
                    "visibility": "listed"
                },
                {
                    "name": "solution",
                    "description": "To escape you have to write, in order:\\n\\n  \\"look mailbox\\"  just to find out it is closed.\\n  \\"open mailbox\\"  to reveal its contents: a leaflet and a key.\\n  \\"look leaflet\\"  to find out how to take the key.\\n  \\"take key\\"      to take the key\\n  \\"look carpet\\"   to find out that it can be dragged.\\n  \\"drag carpet\\"   to reveal a trapdoor beneath.\\n  \\"go trapdoor\\"   to find out that it is closed.\\n  \\"open trapdoor\\" to open it using the golden key.\\n  \\"go trapdoor\\"   to exit the room!",
                    "visibility": "listed"
                }
            ]
        },
        {
            "id": "3",
            "name": "The Great Museum of Architexture",
            "description": "You are in the luxuriuous lobby of the Museum of Architexture. \\n\\nThe corridors extend as far as the eye can see, but wherever you look you only see closed doors with the sign \\"UNDER CONSTRUCTION\\". What a weird museum.\\n\\nYou see a poster that says: \\"LOOK AT ME\\".",
            "exits": [
                {
                    "name": "a ceiling trapdoor",
                    "description": "",
                    "destination_room_id": "2",
                    "visibility": "listed"
                }
            ],
            "items": [
                {
                    "name": "a poster",
                    "description": "WELCOME, ARCHITEXT                            \\n                              \\nI bestbow you with all our knowledge about Architexture. Just write \\"help\\" to see it. There you can learn all that there is to know.\\n\\nEverything you have seen has been created by an architext like you. Did I mention that!? If you don't believe me, write \\"build\\" to start creating a room right here. Or \\"craft\\" to create an item! Its easy :-)\\n\\nThis is just a tiny part of the multiverse. Write \\"exitworld\\" to go to the lobby. There you can go to other worlds and create your own. \\n\\nWhat to do next? Visit the Monk's Riddle world. It is an immersive escape game that lasts 30 to 60 minutes. It is better played by 2-4 people, so invite some friends!\\n\\nThe Monk's Riddle has been built using just the basic tools at \\"help building\\". These are explained in just 20 lines! So it is a great example to learn what you can build.\\n\\nI almost forgot! Join our discord so we can chat!\\nhttps://discord.gg/CnQD9g3U5g\\n\\nThank you so much for playing. Have fun! :-)\\n\\nOliver",
                    "visibility": "listed"
                }
            ]
        }
    ]
}"""