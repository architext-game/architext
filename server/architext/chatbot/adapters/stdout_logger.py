from architext.chatbot.ports.logger import Logger


class StdOutLogger(Logger):
    def log(self, text: str) -> None:
        print(text)