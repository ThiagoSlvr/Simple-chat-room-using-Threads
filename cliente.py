import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog
from random import randrange

# Definimos as constantes inciais
host = '127.0.0.1'
local = 50003

# Função de cores que retorna uma cor aleatoria para customização dos chats
def cores():
    colors = ['lightgreen', 'lightpink', 'lightsalmon2', 'lightblue', 'lightyellow']
    escolhido = randrange(0, 5, 1)
    return colors[escolhido]

# Função para escrever o nome do usuario seguido da mensagem que foi enviada na tela de mensagens e em seguida exclui-la da area de escrita
def escreve():
    mensagem = f"{nome}: {areaInput.get('1.0', 'end')}"
    socket.send(mensagem.encode('utf-8'))
    areaInput.delete('1.0', 'end')

# Função para receber uma mensagem de um outro usuário, que vai ser decoficada, e será escrita na area de mensagens junto do nome do usuario que a enviou
# Também faz com que as mensangens anteriores subam para que a mensagem mais nova fique embaixo
# Além disso lida com possiveis erros de conexão entre outros.
def recebe():
    while rodar:
        try:
            mensagem = socket.recv(1024).decode('utf-8')

            if mensagem == 'NICK':
                socket.send(nome.encode('utf-8'))

            else:
                if interfacePronta:
                    areaTexto.config(state='normal')
                    areaTexto.insert('end', mensagem)
                    areaTexto.yview('end')
                    areaTexto.config(state='disabled')

        except ConnectionAbortedError:
            print("Erro de conexão")
            break

        except:
            print("Erro")
            socket.close()
            break

# Inicializa a conexão com servidor, cria uma janela pedidndo pelo seu nome e inicializa a thread para executar o resto das funções
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((host, local))

mensagem = tkinter.Tk()
mensagem.withdraw()

nome = simpledialog.askstring("Nome", "Digite seu nome", parent = mensagem)
interfacePronta = False
rodar = True

recebeThread = threading.Thread(target=recebe)
recebeThread.start()

cor = cores()

#inicia a janela e define uma cor para o background
janela = tkinter.Tk()
janela.configure(bg=cor)

#desenha na janela um titulo e seu padding
chat_titulo = tkinter.Label(janela, text="Chat:", bg=cor)
chat_titulo.config(font=("Arial", 15))
chat_titulo.pack(padx=20, pady=10)

#define na janela o espaço para as mensagens
areaTexto = tkinter.scrolledtext.ScrolledText(janela)
areaTexto.pack(padx=20, pady=10)
areaTexto.config(state='disabled')
msgPretexto = tkinter.Label(janela, text="Mensagem:", bg=cor)
msgPretexto.config(font=("Arial", 15))
msgPretexto.pack(padx=20, pady=10)

#local para escrever e enviar mensagens
areaInput = tkinter.Text(janela, height=2)
areaInput.pack(padx=20, pady=10)

#botao para enviar a mensagem escrita
botaoEnviar = tkinter.Button(janela, text="Enviar", command=escreve)
botaoEnviar.config(font=("Arial", 15))
botaoEnviar.pack(padx=20, pady=10)

interfacePronta = True

# Inicializa o loop principal a partir da chamada de Tk() da variavel janela
janela.mainloop()