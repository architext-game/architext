from .verb import Verb

class Help(Verb):
    command = 'ayuda'

    def process(self, message):
        help = (
"""Bienvenido a este mundo, donde tienes el poder de dar forma a la realidad.\r
Escribe "mirar" para mirar a tu alrededor.\r
Escribe "decir hola" para decir "hola" a quienes tengas cerca..\r
Escribe "gritar HOLA" para que te oiga todo el mundo.\r
Escribe "emote sonríe" para sonreír. ¡O hacer lo que se te ocurra describir!\r
Escribe "ir puerta" para cruzar una puerta.\r
Escribe "construir" para comenzar a construir una habitación adyacente a donde estás.\r
Escribe "reformar" para modificar la habitación en la que te encuentras.
""")
        self.session.send_to_client(help)

        self.finished = True