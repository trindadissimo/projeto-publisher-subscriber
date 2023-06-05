import socket
import threading

# método __init__ -> construtor que inicializa a classe Servidor.
# -> parâmetros: host e porta, que são o endereço de IP e a porta em que o servidor será executado.
# topics -> dicionário vazio chamado p/ armazenar os tópicos
# -> Lock p/ sincronizar o acesso concorrente às infos compartilhadas.

class Servidor:
    def __init__(self, host, porta):
        self.host = host
        self.porta = porta
        self.topicos = {}
        self.lock = threading.Lock()

    # Cria um socket TCP/IP e faz o bind no endereço e porta especificados.
    # Loop infinito para aceitar conexões de clientes/assinantes.
    # Quando um cliente se conecta, ele cria uma nova thread para lidar com esse cliente usando a função lidar_cliente.
    
    def iniciar(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.porta))
        self.socket.listen(5)
        print(f"Servidor executando em {self.host}:{self.porta}...")

        while True:
            cliente_socket, endereco = self.socket.accept()
            thread_cliente = threading.Thread(target=self.lidar_cliente, args=(cliente_socket,))
            thread_cliente.start()

    # Método lidar_cliente é responsável pela conexão de um cliente. 
    # Recebe o socket do cliente como parâmetro. (recebe uma msg do cliente para identificar se é um publicador ou um assinante. 
    # Com base no tipo de cliente, ele chama os métodos lidar_publicador ou lidar_assinante para tratar as msgs.
    # Após o processamento, o socket do cliente é fechado.

    def lidar_cliente(self, cliente_socket):
        tipo_cliente = cliente_socket.recv(1024).decode()
        if tipo_cliente == "publicador":
            self.lidar_publicador(cliente_socket)
        elif tipo_cliente == "assinante":
            self.lidar_assinante(cliente_socket)
        cliente_socket.close()

    # lidar_publicador trata as msgs enviadas por um cliente publicador(publicher).
    # Recebe o socket do publicador como parâmetro.
    # Recebe o tópico do publicador. 
    # Chama o método adicionar_topico p/ garantir que o tópico esteja registrado no server.
    # Entra em um loop infinito para receber as mensagens do publicador.
    # Se uma msg for recebida, ela é impressa no console juntamente com o tópico correspondente.
    # Essa msg é armazenada usando o método armazenar_mensagem.

    def lidar_publicador(self, publicador_socket):
        topico = publicador_socket.recv(1024).decode()
        self.adicionar_topico(topico)
        print(f"Novo publicador conectado: {topico}")

        while True:
            mensagem = publicador_socket.recv(1024).decode()
            if not mensagem:
                break
            print(f"Mensagem recebida de {topico}: {mensagem}")
            self.armazenar_mensagem(topico, mensagem)

    # método lidar_assinante trata as msgs enviadas por um cliente assinante (subscriber). 
    # recebe o socket do assinante como parâmetro. 
    # recebe o tópico do assinante. 
    # chama o método adicionar_topico p/ garantir que o tópico esteja registrado no server. 
    # chama o método enviar_ultima_mensagem para enviar a última mensagem armazenada no tópics para o assinante.

    def lidar_assinante(self, assinante_socket):
        topico = assinante_socket.recv(1024).decode()
        self.adicionar_topico(topico)
        print(f"Novo assinante conectado: {topico}")

        self.enviar_ultima_mensagem(assinante_socket, topico)

    def adicionar_topico(self, topico):
        with self.lock:
            if topico not in self.topicos:
                self.topicos[topico] = []

    def armazenar_mensagem(self, topico, mensagem):
        with self.lock:
            self.topicos[topico].append(mensagem)

    # método enviar_ultima_mensagem envia a última msg armazenada em um tópico para um assinante específico. 
    # utiliza o lock para garantir o acesso exclusivo ao dicionário topicos.
    # se o tópico existir no dicionário e se possui mensagens armazenadas, ele obtém a última mensagem da lista e a envia para o assinante.

    def enviar_ultima_mensagem(self, assinante_socket, topico):
        with self.lock:
            if topico in self.topicos and self.topicos[topico]:
                ultima_mensagem = self.topicos[topico][-1]
                assinante_socket.send(ultima_mensagem.encode())

    def fechar(self):
        self.socket.close()

if __name__ == "__main__":
    servidor = Servidor("localhost", 55555)
    servidor.iniciar()