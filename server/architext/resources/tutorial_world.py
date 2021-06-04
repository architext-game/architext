from .. import util

json = util.remove_control_characters(r"""
{"next_room_id": 4, "starting_room": {"name": "The Legs Lab", "alias": "0", "description": "You
awake in a white room. A robotic voice says:\r\n\r\nWelcome, Architext. My purpose is to awake your 
virtual limbs and senses. Please listen carefully. Now type \"go door\" to use your legs.", 
"custom_verbs": [], "items": []}, "other_rooms": [{"name": "The Eyes Lab", "alias": "1", 
"description": "You cross the door into another cubic room. The wall in front of you is covered by a 
huge curtain.\r\nIt has a big writing on it: \r\n\r\nIf your virtual eyes work, enter \"look 
curtain\".", "custom_verbs": [], "items": [{"item_id": null, "name": "a big white curtain", 
"description": "You get a closer look at the curtain and find that there is a black door behind it! 
Maybe you can go through it?", "visible": "listed", "custom_verbs": []}]}, {"name": "The Hands Lab", 
"alias": "2", "description": "The voice talks again as you cross into the next 
room:\r\n\r\nCongrats! Let's see if you can find the exit of this one. Make me happy again.
\r\n\r\nAn old oriental carpet covers the aseptic floor of the lab room. Oddly enough, there is a 
small\r\nmailbox next to it. They clearly don't belong here.", "custom_verbs": [], "items": 
[{"item_id": null, "name": "a small mailbox", "description": "It appears to be something inside, but 
the mailbox is closed!", "visible": "obvious", "custom_verbs": [{"names": ["open"], "commands": 
["textto '.user' You open the mailbox and find a leaflet and a key inside.", "deleteitem a small 
mailbox", "spawn a small mailbox#2", "spawn a leaflet#1", "spawn a golden key#1"]}]}, {"item_id": 
null, "name": "an old carpet", "description": "It is worn out and grubby. In fact, you have the 
impression that the carpet has been dragged out of place many, many times.", "visible": "obvious", 
"custom_verbs": [{"names": ["move", "drag", "pull", "displace", "remove"], "commands": ["textto '.
user' You manage to move the heavy carpet and discover a hidden trapdoor beneath it.", "edit 
trapdoor", "2", "listed", "deleteitem an old carpet", "spawn an old carpet#2"]}]}]}, {"name": "The 
Great Museum of Architexture", "alias": "3", "description": "You are in the luxuriuous lobby of the 
Museum of Architexture. \r\n\r\nThe corridors extend as far as the eye can see, but wherever you 
look you only see closed doors with the sign \"UNDER CONSTRUCTION\". What a weird museum.\r\n\r\nYou 
see a poster that says: \"LOOK AT ME\".", "custom_verbs": [], "items": [{"item_id": null, "name": "a 
poster", "description": "_ _ _     _                        _____         _   _ _           _   
\r\n| | | |___| |___ ___ _____ ___     |  _  |___ ___| |_|_| |_ ___ _ _| |_ \r\n| | | | -_| |  _| . 
|     | -_|_   |     |  _|  _|   | |  _| -_|_'_|  _|\r\n|_____|___|_|___|___|_|_|_|___| |  |__|__|_| 
|___|_|_|_|_| |___|_,_|_|  \r\n                              |_|                                     
\r\n                              \r\nI bestbow you with all our knowledge about Architexture. Just 
write \"help\" to see it. There you can learn all that there is to know.\r\n\r\nEverything you have 
seen has been created by an architext like you. Did I mention that!? If you don't believe me, write 
\"build\" to start creating a room right here. Or \"craft\" to create an item! Its easy :-
)\r\n\r\nThis is just a tiny part of the multiverse. Write \"exitworld\" to go to the lobby. There 
you can go to other worlds and create your own. \r\n\r\nWhat to do next? Visit the Monk's Riddle 
world. It is an immersive escape game that lasts 30 to 60 minutes. It is better played by 2-4 people,
so invite some friends!\r\n\r\nThe Monk's Riddle has been built using just the basic tools at \"help 
build\". These are explained in just 20 lines! So it is a great example to learn what you can build.
\r\n\r\nThank you so much for playing. Have fun! :-)", "visible": "listed", "custom_verbs": []}]}], 
"custom_verbs": [], "exits": [{"name": "a white metal door", "description": null, "destination": "1",
"room": "0", "visible": "listed", "is_open": true, "key_names": []}, {"name": "back to the Legs Lab",
"description": null, "destination": "0", "room": "1", "visible": "listed", "is_open": true, 
"key_names": []}, {"name": "a black door", "description": null, "destination": "2", "room": "1", 
"visible": "hidden", "is_open": true, "key_names": []}, {"name": "back to the Eyes Lab", 
"description": null, "destination": "1", "room": "2", "visible": "listed", "is_open": true, 
"key_names": []}, {"name": "a trapdoor", "description": null, "destination": "3", "room": "2", 
"visible": "hidden", "is_open": false, "key_names": ["a golden key"]}, {"name": "a ceiling trapdoor",
"description": null, "destination": "2", "room": "3", "visible": "listed", "is_open": true, 
"key_names": []}], "inventory": [], "saved_items": [{"item_id": "a small mailbox#1", "name": "a 
small mailbox", "description": "It appears to be something inside, but the mailbox is closed!", 
"visible": "listed", "custom_verbs": [{"names": ["open"], "commands": ["textto '.user' You open the 
mailbox and find a leaflet and a key inside.", "deleteitem a small mailbox", "spawn a small 
mailbox#2", "spawn a leaflet#1", "spawn a golden key#1"]}]}, {"item_id": "a leaflet#1", "name": "a 
leaflet", "description": "The leafleat reads:\r\n\r\nWelcome, subject. I'm sorry about all of this 
weird robot lab stuff, but we need to test your functions before you can consider yourself an 
architext.\r\n\r\nI hope you find this key useful. Try to use your hands to take it writing \"take 
key\".\r\n\r\nAnd don't forget to have a look at the beautiful carpet!", "visible": "takable", 
"custom_verbs": []}, {"item_id": "a golden key#1", "name": "a golden key", "description": "It 
sparkles with life.", "visible": "takable", "custom_verbs": []}, {"item_id": "a small mailbox#2", 
"name": "a small mailbox", "description": "It's now open.", "visible": "listed", "custom_verbs": []},
{"item_id": "an old carpet#1", "name": "an old carpet", "description": "It is worn out and grubby. 
In fact, you have the impression that the carpet has been dragged out of place many, many times.", 
"visible": "obvious", "custom_verbs": [{"names": ["move", "drag", "pull", "displace", "remove"], 
"commands": ["textto '.user' You manage to move the heavy carpet and discover a hidden trapdoor 
beneath it.", "edit trapdoor", "2", "listed", "deleteitem an old carpet", "spawn an old 
carpet#2"]}]}, {"item_id": "an old carpet#2", "name": "an old carpet", "description": "It has been 
moved to the side.", "visible": "obvious", "custom_verbs": []}]}
""")