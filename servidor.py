import threading
import socket

# Comandos para limpar as portas, caso estejam ocupadas
#fuser -k 50000/tcp - limpa socket
#lsof -i :50000 - verifica socket

host = "localhost"

local = 50003

#define e inicia server como tcp
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,local))
server.listen()

#cria lista de clientes
clientes=[]

#cria lista para os nomes
nomes=[]

#função para enviar mensagem para todos clientes
def enviar(mensagem):

    for cliente in clientes:

        cliente.send(mensagem)

#gerencia novas mensagens
def gerenciar(cliente):

    while True:

        try:

            #recebe mensagem do cliente
            mensagem = cliente.recv(1024)
            enviar(mensagem)

        except:

            #caso receba algo diferente de uma mensagem exclui o cliente
            index = clientes.index(cliente)

            clientes.pop(index)
            cliente.close()
            nomes.pop(index)
            break

#gerenciar novos clientes
def receber():
    
    while True:
        
        cliente, address = server.accept()
        cliente.send("NICK".encode())

        #recebe o nome do cliente e salva seus dados em duas listas
        nickname = cliente.recv(1024).decode()
        nomes.append(nickname)
        clientes.append(cliente)
    
        #cria e inicia thread para cada cliente adicionado
        thread = threading.Thread(target=gerenciar, args=(cliente,))
        thread.start()

receber()