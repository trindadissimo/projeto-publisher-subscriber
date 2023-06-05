import socket

class Publicador:
    def __init__(self, host, porta):
        self.host = host
        self.porta = porta

    def iniciar(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.porta))

        self.socket.send("publicador".encode())

        topico = input("Tópico: ")
        self.socket.send(topico.encode())

        while True:
            mensagem = input("Texto: ")
            self.socket.send(mensagem.encode())

    def fechar(self):
        self.socket.close()

if __name__ == "__main__":
    publicador = Publicador("localhost", 55555)
    publicador.iniciar()