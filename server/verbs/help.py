from .verb import Verb

class Help(Verb):
    """Shows a help message to the user"""

    command = 'ayuda'

    def process(self, message):
        help = (
"""Bienvenido a este mundo, donde tienes el poder de dar forma a la realidad.
Estos son las acciones que puedes escribir en el juego:

BÁSICAS
  - "mirar" para mirar a tu alrededor.
  - "mirar <nombre del objeto/salida>" para mirar de cerca un objeto o una salida.
  - "ir <salida>" para cruzar una salida.
  - "salidas" para ver las salidas OBVIAS de tu habitación.
  - "objetos" para ver los objetos OBVIOS de tu habitación.

AVANZADAS
  - "coger <objeto>" coge un objeto. Nota: no todos pueden cogerse.
  - "dejar <objeto>" deja un objeto de tu inventario en la sala actual.
  - "inventario" muestras los objetos de tu inventario.
  - "abrir <salida>" intenta abrir una salida cerrada. Deberás tener la llave en tu inventario.
  
COMUNICACIÓN
  - "decir <mensaje>" enviar un mensaje a todos los que estén en tu misma localización.
  - "gritar <mensaje>" para enviar un mensaje a todos.
  - "emote <acción>" para hacer una acción, y que todos los que están contigo lo vean.

CONSTRUCCIÓN SENCILLA
  - "construir" para construir una habitación adyacente a donde estás.
  - "fabricar" para crear un objeto en la habitación donde estás.
  - "reformar" para modificar la habitación en la que te encuentras.
  - "editar <nombre del objeto/salida>" para modificar un objeto o salida de tu habitación.

CONSTRUCCIÓN AVANZADA
  - "info" para ver toda la información de la habitación donde estás.
  - "info <nombre del objeto/salida> para ver la info de un objeto o salida de tu habitación.
  - "conectar" para conectar la sala donde estás con otra sala.
      (Necesitarás el alias de la sala, usa el comando "info")
  - "eliminarsala" para borrar la sala donde estás. SIN REMEDIO.
  - "eliminarsalida <nombre de la salida>" para borrar una salida. SIN REMEDIO.
  - "eliminarobjeto <nombre del objeto>" para borrar un objeto. SIN REMEDIO.
  - "tp <alias de la sala>" para transportarte a cualquier sala.
      (El alias puedes consultarlo con el comando "info")

CONSTRUCCIÓN INTERACTIVA
  - "verboobjeto <objeto>" añade un verbo a un objeto.
  - "verbosala" añade un verbo a la sala actual.
  - "verbomundo" añade un verbo en todo el mundo.
  - "guardar <objeto>" para guardar una copia de un objeto que esté en tu sala.
  - "colocar <id del objeto>" para colocar un objeto previamente guardado.

LLAVES
  - "cierradirector <salida>" para cerrar una salida. No podrá cruzarse.
  - "abredirector <salida>" para abrir una salida.
  - "asignarllave <salida>" para hacer que un objeto pueda abrir una salida.

MODO DIRECTOR
 - "director" para entrar y salir del modo director. Que permite:
    > cruzar puertas cerradas
    > ser invisible a los demás jugadores
""")
        self.session.send_to_client(help)

        self.finish_interaction()