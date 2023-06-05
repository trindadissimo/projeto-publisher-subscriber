import socket

class Assinante:
    def __init__(self, host, porta):
        self.host = host
        self.porta = porta

    def iniciar(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.porta))

        self.socket.send("assinante".encode())

        topico = input("Digite o tópico: ")
        self.socket.send(topico.encode())

        ultima_mensagem = self.socket.recv(1024).decode()
        if ultima_mensagem:
            print("Última mensagem do tópico selecionado:", ultima_mensagem)

        while True:
            mensagem = self.socket.recv(1024).decode()
            if not mensagem:
                break
            print("Mensagem recebida:", mensagem)

    def fechar(self):
        self.socket.close()

if __name__ == "__main__":
    assinante = Assinante("localhost", 55555)
    assinante.iniciar()