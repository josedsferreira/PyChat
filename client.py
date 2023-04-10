import socket
from threading import Thread
from datetime import datetime
from tkinter import *

# IP do servidor
SERVER_HOST = "127.0.0.1" #localhost é 127.0.0.1
SERVER_PORT = 5002 # server's port

# inicializar TCP socket
s = socket.socket()
# conectar ao server
s.connect((SERVER_HOST, SERVER_PORT))

class GUI:
    # constructor method
    def __init__(self):
        """
        função que inicializa os atributos da classe e assim como a janela de login
        recebe o nome do cliente e posteriormente envia o nome para a função começar
        """

        # janela do chat, escondida até o deiconify
        self.Window = Tk()
        self.Window.withdraw()

        # janela de login
        self.login = Toplevel()
        # Escolher o titulo
        self.login.title("Login")
        self.login.iconbitmap("icon.ico")
        self.login.resizable(width=False,height=False)
        window_width = 300
        window_height = 200
        self.login.configure(width=window_width,height=window_height)

        # get the screen dimension
        screen_width = self.login.winfo_screenwidth()
        screen_height = self.login.winfo_screenheight()

        # find the center point
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)

        #colocar no centro do ecra
        self.login.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        # label de instruçao
        self.pf = Label(self.login, text="Por favor insira o seu nome para continuar:", justify=CENTER)
        self.pf.place(relheight=0.15, relx=0.1, rely=0.07)

        # Label do nome
        #self.labelNome = Label(self.login, text="Nome: ")
        #self.labelNome.place(relheight=0.3, relx=0.1, rely=0.1)

        # entry box para o nome
        self.entryNome = Entry(self.login)
        self.entryNome.place(relwidth=0.4, relheight=0.12, relx=0.3, rely=0.2)

        # foco na caixa
        self.entryNome.focus()

        # Botao de ação para avançar
        self.continuar = Button(self.login, text="Continuar",  command=lambda: self.comecar(self.entryNome.get()))
        self.continuar.place(relx=0.4, rely=0.55)

        self.Window.mainloop()

    def comecar(self, name):
            """
            função que destroi a pagina de login e cria a pagina de chat
            cria uma thread para receber as mensagens passadas e imprimir
            """

            self.login.destroy() #destroi a pagina de login e cria a do menu principal(layout)
            self.layout(name)

            #criar um thread que fica a espera de mensagens para este cliente e imprime
            t = Thread(target=self.receber)
            #torna um thread um daemon thread para que termine sempre que o main thread termine
            t.daemon = True
            # começa o thread
            t.start()

    # Janela principal do chat
    def layout(self, name):
        """
        função que cria todo o ambiente grafico do chat
        sendo possível escrever mensagens na caixa de texto destinada,visualizar mensagens e enviar mensagens
        é disponibilizada a informação de mensagem, isto é a hora que foi enviada e quem a escreveu
        """

        self.name = name #nome do utilizador
        
        #janela principal
        self.Window.deiconify() #faz aparecer a janela
        self.Window.title("PyChat")
        self.Window.iconbitmap("icon.ico")
        self.Window.resizable(width=True, height=True)
        window_width = 600
        window_height = 550
        self.Window.configure(width=window_width, height=window_height)
        # get the screen dimension
        screen_width = self.Window.winfo_screenwidth()
        screen_height = self.Window.winfo_screenheight()
        # find the center point
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)
        #colocar no centro do ecra
        self.Window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        #nome no topo da janela
        self.labelHead = Label(self.Window, text=self.name, pady=5) 
        self.labelHead.place(relwidth=1)

        #janela onde as mensagens vao aparecer
        self.textCons = Text(self.Window, width=20, height=2, padx=5, pady=5) 
        self.textCons.place(relheight=0.745, relwidth=1, rely=0.08)

        #label onde estara a caixa de texto
        self.labelFundo = Label(self.Window, height=80) 
        self.labelFundo.place(relwidth=1, rely=0.825)

        #caixa de texto para a mensagem
        self.entryMsg = Entry(self.labelFundo) 
        self.entryMsg.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.entryMsg.focus()

        # botao de envio
        self.botaoMsg = Button(self.labelFundo, text="Enviar", width=20, command=lambda: self.BotaoEnviar(self.entryMsg.get()))
        self.botaoMsg.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)

        # scroll bar
        scrollbar = Scrollbar(self.textCons)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.config(command=self.textCons.yview)

        self.textCons.config(state=DISABLED)

        
    # função para iniciar thread de envio de mensagem
    def BotaoEnviar(self, msg):
        """
        Função que começa o envio da mensagem
        """
        self.textCons.config(state=DISABLED) #torna nao responsivo a comandos
        self.msg = msg
        self.entryMsg.delete(0, END)
        enviar = Thread(target=self.enviarMsg)
        enviar.start()

    # funçao para receber as mensagens
    def receber(self):
        """
        função que recebe as mensagens mensagens
        """

        while True:
            try:
                message = s.recv(1024).decode()

                # Insere a mensagem no textCons
                self.textCons.config(state=NORMAL) #torna responsivo a comandos
                self.textCons.insert(END, message +"\n\n") #end é o local onde inserir

                self.textCons.config(state=DISABLED)
                self.textCons.see(END) #move o cursor
            except:
                print("Ocorreu um erro!")
                s.close()
                break

    # funcao para enviar mensagens
    def enviarMsg(self):
        """
        função que codifica e envia as mensagens
        """
        self.textCons.config(state=DISABLED)

        date_now = datetime.now().strftime('%H:%M') 
        message = (f"[{date_now}]{self.name}: {self.msg}")
        s.send(message.encode())


gui = GUI()