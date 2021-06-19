from .. import util

json = util.remove_control_characters(r"""
{
    "next_room_id": 4,
    "starting_room": {
        "name": "El Laboratorio Motriz",
        "alias": "0",
        "description": "Despiertas en una habitación blanca. Una voz robótica dice:\r\n\r\nBienvenido, arquitexto. Mi propósito es despertar tus capacidades motrices y sensoriales. Por favor, escucha con atención.\r\n\r\nCuando estés listo, escribe \"ir puerta\" para utilizar tus piernas por primera vez.",
        "custom_verbs": [],
        "items": []
    },
    "other_rooms": [
        {
            "name": "El Laboratorio Visual",
            "alias": "1",
            "description": "Cruzas la puerta hasta otra sala cúbica. El muro frente a ti está cubierto por una gruesa cortina.\r\n\r\nLa voz robótica dice: Para comprobar si tus ojos virtuales están operativos, escribe \"mirar cortina\".",
            "custom_verbs": [],
            "items": [
                {
                    "item_id": null,
                    "name": "una gruesa cortina",
                    "description": "Al acercarte para examinar la cortina descubres que hay un pasillo oculto detrás de ella. Quizá puedas ir por ahí.\r\n\r\nPuedes escribir \"ir <salida>\" para ir hacia cualquier salida en tu habitación.",
                    "visible": "obvious",
                    "custom_verbs": []
                }
            ]
        },
        {
            "name": "The Hands Lab",
            "alias": "2",
            "description": "Felicidades! Veamos si puedes salir de esta última sala. Puedes escribir \"mirar <objeto>\" para investigar cualquier cosa que veas aquí.\r\n\r\nUna vieja alfombra oriental cubre el suelo aséptico del laboratorio. Extrañamente, hay un pequeño buzón a su lado. Está claro que no encajan en este lugar.\r\n\r\nVes un poster con pistas que pueden ayudate a escapar. Escribe \"mirar poster\" solo si estás atascado.",
            "custom_verbs": [],
            "items": [
                {
                    "item_id": null,
                    "name": "un pequeño buzón",
                    "description": "Parece haber algo dentro del buzón, pero está cerrado. Quizá deberías probar con \"abrir buzón\"?",
                    "visible": "obvious",
                    "custom_verbs": [
                        {
                            "names": [
                                "abrir"
                            ],
                            "commands": [
                                "textoa '.user' Abres el buzón. Dentro encuentras una llave dorada y un folleto.",
                                "borrarobjeto un pequeño buzón",
                                "colocar un pequeño buzón#2",
                                "colocar un folleto#1",
                                "colocar una llave dorada#1"
                            ]
                        }
                    ]
                },
                {
                    "item_id": null,
                    "name": "una vieja alfombra",
                    "description": "Está gastada y sucia. Las arrugas que tiene te hacen pensar que ha sido levantada muchas, muchas veces.",
                    "visible": "obvious",
                    "custom_verbs": [
                        {
                            "names": [
                                "levantar",
                                "mover",
                                "quitar",
                                "arrastrar",
                                "levanto",
                                "desplazar",
                                "retirar"
                            ],
                            "commands": [
                                "textoa '.user' Al retirar la pesada alfombra descubres una trampilla escondida debajo de ella.",
                                "editar trampilla",
                                "2",
                                "listed",
                                "borrarobjeto una vieja alfombra",
                                "colocar una vieja alfombra#2"
                            ]
                        }
                    ]
                },
                {
                    "item_id": null,
                    "name": "un póster",
                    "description": "LEE SOLO HASTA DONDE NECESITES!\r\n\r\nUsa el verbo \"mirar <objeto>\" para mirar a cualquier objeto de la sala (el buzón, por ejemplo).\r\n\r\nLee cuidadosamente la descripción de los objetos que mires. Te dirán cómo continuar.\r\n\r\nSi encuentras un folleto, míralo también!\r\n\r\nAtento a la alfombra: tendrás que hacer algo con ella (además de mirarla) para avanzar.\r\n\r\nSi parece que no puedes abrir algo quizá sea porque necesitas coger una llave primero.\r\n\r\nSi sigues atascado y necesitas saber qué hacer exactamente, escribe \"mirar solución\".",
                    "visible": "obvious",
                    "custom_verbs": []
                },
                {
                    "item_id": null,
                    "name": "solución",
                    "description": "Para escapar debes escribir, en orden: \r\n\r\n\"mirar buzón\"       para descubrir que está cerrado.\r\n\"abrir buzón\"       para revelar sus contenidos: un folleto y una llave.\r\n\"mirar folleto\"     para descubrir cómo coger la llave.\r\n\"coger llave\"       para coger la llave.\r\n\"mirar alfombra\"    para descubrir que se puede levantar.\r\n\"levantar alfombra\" para revelar una trampilla oculta bajo ella.\r\n\"ir trampilla\"      para descubrir que está cerrada.\r\n\"abrir trampilla\"   para abrirla usando la llave dorada.\r\n\"ir trampilla\"      para salir de la habitación!",
                    "visible": "hidden",
                    "custom_verbs": []
                }
            ]
        },
        {
            "name": "El Gran Museo de Arquitextura",
            "alias": "3",
            "description": "Te encuentras en el lujoso recibidor del museo de Arquitextura.\r\n\r\nLos anchos pasillos se extienden hasta donde alcanza la vista, pero allá donde miras solo ves puertas cerradas con el cartel \"EN CONSTRUCCIÓN\". Que museo tan extraño.\r\n\r\nVes un póster que dice \"MÍRAME\".",
            "custom_verbs": [],
            "items": [
                {
                    "item_id": null,
                    "name": "un póster",
                    "description": "
               _____ _                     _   _       \r\n
              | __  |_|___ ___ _ _ ___ ___|_|_| |___   \r\n
              | __ -| | -_|   | | | -_|   | | . | . |_ \r\n
              |_____|_|___|_|_|\\_/|___|_|_|_|___|___| |\r\n
               _____             _ _           _    |_|\r\n
              |  _  |___ ___ _ _|_| |_ ___ _ _| |_ ___ \r\n
              |     |  _| . | | | |  _| -_|_'_|  _| . |\r\n
              |__|__|_| |_  |___|_|_| |___|_,_|_| |___|\r\n
                          |_| \r\n\r\nTe confío todo nuestro conocimiento sobre Arquitextura. Símplemente escribe \"ayuda\" para descubrirlo.\r\n\r\nTodo lo que has visto hasta ahora ha sido creado por un arquitexto como tú. ¿¡Qué te parece!? Si no me crees, escribe \"construir\" para crear tu primera  sala aquí mismo. O \"fabricar\" para crear un objeto! Así de fácil :-)\r\n\r\nEste mundo es solo una pequeña parte del multiverso. Escribe \"salirmundo\" para ir al lobby. Desde allí puedes viajar a mundos creados por otros jugadores o crear el tuyo.\r\n\r\nQué puedes hacer ahora? Una buena idea es visitar el mundo \"El Enigma del Monasterio\". Es un juego de escape inmersivo que dura entre 30 y 60 minutos. Es mejor jugarlo de 2 a 4  jugadores, invita a tus amigos!\r\n\r\nEl Enigma del Monasterio ha sido creado usando solamente las herramientas básicas que encontrarás si escribes \"ayuda construir\", explicadas en solo 20 líneas. Por eso, el Monasterio es un gran ejemplo para aprender qué clase de cosas puedes crear con esas sencillas herramientas, e inspirarte para crear tus propios mundos.\r\n\r\nCasi se me olvida! Únete a nuestro canal de discord para que podamos charlar un rato :-) (Busca el canal en Español!)\r\nhttps://discord.gg/CnQD9g3U5g\r\n\r\nGracias por jugar. Diviértete!\r\n\r\nOliver",
                    "visible": "listed",
                    "custom_verbs": []
                }
            ]
        }
    ],
    "custom_verbs": [],
    "exits": [
        {
            "name": "una puerta blanca",
            "description": null,
            "destination": "1",
            "room": "0",
            "visible": "listed",
            "is_open": true,
            "key_names": []
        },
        {
            "name": "de vuelta al Laboratorio Motriz",
            "description": null,
            "destination": "0",
            "room": "1",
            "visible": "obvious",
            "is_open": true,
            "key_names": []
        },
        {
            "name": "un pasillo oculto",
            "description": null,
            "destination": "2",
            "room": "1",
            "visible": "hidden",
            "is_open": true,
            "key_names": []
        },
        {
            "name": "de vuelta al Laboratorio Visual",
            "description": null,
            "destination": "1",
            "room": "2",
            "visible": "obvious",
            "is_open": true,
            "key_names": []
        },
        {
            "name": "una trampilla",
            "description": null,
            "destination": "3",
            "room": "2",
            "visible": "hidden",
            "is_open": false,
            "key_names": [
                "una llave dorada"
            ]
        },
        {
            "name": "una trampilla en el techo",
            "description": null,
            "destination": "2",
            "room": "3",
            "visible": "listed",
            "is_open": true,
            "key_names": []
        }
    ],
    "inventory": [],
    "saved_items": [
        {
            "item_id": "un pequeño buzón#1",
            "name": "un pequeño buzón",
            "description": "Parece haber algo dentro del buzón, pero está cerrado. Quizá deberías probar con \"abrir buzón\"?",
            "visible": "listed",
            "custom_verbs": [
                {
                    "names": [
                        "open"
                    ],
                    "commands": [
                        "textoa '.user' Abres el buzón. Dentro encuentras una llave dorada y un folleto.",
                        "borrarobjeto un pequeño buzón",
                        "colocar un pequeño buzón#2",
                        "colocar un folleto#1",
                        "colocar una llave dorada#1"
                    ]
                }
            ]
        },
        {
            "item_id": "un folleto#1",
            "name": "un folleto",
            "description": "El folleto dice:\r\n\r\nBienvenido, sujeto. Te pido disculpas personalmente por haberte encerrado en este laboratorio. Necesitamos probar tus funciones antes de que puedas vagar libremente como arquitexto.\r\n\r\nEspero que esta llave te sea de utilidad. Intenta usar tus manos para cogerla escribiendo \"coger llave\".\r\n\r\nY no olvides echar un vistazo a nuestra exótica alfombra!",
            "visible": "takable",
            "custom_verbs": []
        },
        {
            "item_id": "una llave dorada#1",
            "name": "una llave dorada",
            "description": "Centellea con brillos dorados. Parece importante.",
            "visible": "takable",
            "custom_verbs": []
        },
        {
            "item_id": "un pequeño buzón#2",
            "name": "un pequeño buzón",
            "description": "Está abierto.",
            "visible": "obvious",
            "custom_verbs": []
        },
        {
            "item_id": "una vieja alfombra#1",
            "name": "una vieja alfombra",
            "description": "Está gastada y sucia. Las arrugas que tiene te hacen pensar que ha sido levantada muchas, muchas veces.",
            "visible": "obvious",
            "custom_verbs": [
                {
                    "names": [
                        "levantar",
                        "mover",
                        "quitar",
                        "arrastrar",
                        "levanto",
                        "desplazar",
                        "retirar"
                    ],
                    "commands": [
                        "textoa '.user' Al retirar la pesada alfombra descubres una trampilla escondida debajo de ella.",
                        "editar trampilla",
                        "2",
                        "listado",
                        "borrarobjeto una vieja alfombra",
                        "colocar una vieja alfombra#2"
                    ]
                }
            ]
        },
        {
            "item_id": "una vieja alfombra#2",
            "name": "una vieja alfombra",
            "description": "La has dejado arrugada a un lado.",
            "visible": "obvious",
            "custom_verbs": []
        }
    ]
}
""")