from .verb import Verb

class Help(Verb):
    command = 'ayuda'

    def process(self, message):
        help = (
"""Bienvenido a este mundo, donde tienes el poder de dar forma a la realidad.
Estos son las acciones que puedes escribir en el juego:

BÁSICAS
  - "mirar" para mirar a tu alrededor.
  - "mirar <nombre del objeto>" para mirar un objeto de cerca.
  - "ir <salida>" para cruzar una salida.
  - "decir <mensaje>" enviar un mensaje a todos los que estén en tu misma localización.
  - "gritar <mensaje>" para enviar un mensaje a todos.
  - "emote <acción>" para hacer una acción, y que todos los que están contigo lo vean.

CONSTRUCCIÓN SENCILLA
  - "construir" para construir una habitación adyacente a donde estás.
  - "fabricar" para crear un objeto en la habitación donde estás.
  - "reformar" para modificar la habitación en la que te encuentras.
  - "editar <nombre del objeto>" para modificar un objeto de tu habitación.

CONSTRUCCIÓN AVANZADA
  - "info" para ver toda la información de la habitación donde estás.
  - "info <nombre del objeto> para ver la info de un objeto de tu habitación.
  - "conectar" para conectar la sala donde estás con otra sala.
    - (Necesitarás el alias de la sala, usa el comando "info")
  - "eliminarsala" para borrar la sala donde estás. SIN REMEDIO.
  - "eliminarsalida <nombre de la salida>" para borrar una salida.
  - "eliminarobjeto <nombre del objeto>" para borrar un objeto.
  - "tp <alias de la sala>" para transportarte a cualquier sala.
    - (El alias puedes consultarlo con el comando "info")
""")
        self.session.send_to_client(help)

        self.finished = True