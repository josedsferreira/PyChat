import socket
from threading import Thread

# IP do servidor
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5002 # porta que queremos usar

class log():
    
    def writelog(self, msg):
        """
        Regista as mensagens num ficheiro
        """
        with open("log.txt", 'a') as log:
            log.write(msg + "\n\n")

    def logsend(self, cs):
        with open("log.txt", 'r') as log:
            for line in log:
                cs.send(line.encode())


class server():

    def __init__(self, SERVER_HOST, SERVER_PORT):
        self.SERVER_HOST = SERVER_HOST
        self.SERVER_PORT = SERVER_PORT
        #inicializa todos os sockets dos clientes conectados
        self.client_sockets = set()
        # criar TCP socket
        self.s = socket.socket()
        # tornar o port reutilizavel
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # bind do socket ao endereço
        self.s.bind((self.SERVER_HOST, self.SERVER_PORT))
        # Esperar por conexoes
        self.s.listen(5)
        print(f"[*] Listening as {self.SERVER_HOST}:{self.SERVER_PORT}")

    def listen_for_client(self, cs):
        """
        função que fica a espera de mensagens vindas do socket cs
        quando mensagem é recebida é enviada a todos os clientes conectados
        """
        while True:
            try:
                #fica a espera de uma mensagem do socket cs
                msg = cs.recv(1024).decode()
            except Exception as e:
                # cliente ja nao esta conectado, remover da lista
                print(f"[!] Error: {e}")
                self.client_sockets.remove(cs)
            else:
                #escrever mensagem no log:
                logfile = log()
                logfile.writelog(msg)
                # iterate iterar pelos sockets conectados e enviar mensagem
            for client_socket in self.client_sockets:
                client_socket.send(msg.encode())

    def connect_client(self):
        """
        Função que conecta o cliente novo e envia lhe o registo das mensagens
        """
        while True:
            #esta sempre a espera de novas conecçoes
            client_socket, client_address = self.s.accept()
            print(f"[+] {client_address} connected.")

            #enviar log para o cliente
            log1 = log()
            log1.logsend(client_socket)

            # adiciona novo cliente aos sockets conectados
            self.client_sockets.add(client_socket)

            #começa um novo thread que espera pelas mensagens de cada cliente
            t = Thread(target=self.listen_for_client, args=(client_socket,)) #args é um tupple
            
            #torna o thread um thread daemon para que termine se o main thread terminar
            t.daemon = True
            # iniciar o thread
            t.start()

    def terminar(self):
        """
        Função para fechar todos os sockets
        """
        # terminar sockets dos clientes
        for cs in self.client_sockets:
            cs.close()
        # fechar socket do servidor
        self.s.close()

servidor = server(SERVER_HOST, SERVER_PORT)
servidor.connect_client()