#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

destino = ''

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Greetings from the cave! Now type your name and press enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    nome =''
    mensagem=''

    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Bem-vindo %s! Se você quiser sair, digite quit().' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        print(msg)
        if msg == bytes("listar()","utf8"):
            client.send(bytes("lista de usuarios:\n","utf8"))
            for i,v in clients.items():
                client.send(bytes("Nome: "+ str(v) + ", IP: " +str(i.getpeername()[0]) + ", PORT:" + str(i.getpeername()[1]) +"\n","utf8")) 
            #client.send(bytes(msg,"utf8"))
        elif msg[:5] == bytes("nome(","utf8") and chr(msg[len(msg) - 1]) == ")":
            clients[client] = msg[5:-1].decode("utf8")
            broadcast(bytes("%s alterou o nome para %s." %(name,msg[5:-1].decode("utf8")), "utf8"))
            name = msg[5:-1].decode("utf8")
        elif msg[:8] == bytes("privado(","utf8") and chr(msg[len(msg) - 1]) == ")":
            index = 99999           
            for i in range(len(msg)):
                if "," == chr(msg[i]):
                    index = i
                    break
            nome = msg[8:index]
            mensagem = bytes("PRIVADO[","utf8") + nome + bytes("]:","utf8") + msg[index + 1:-1]
            for i in range(len(clients)):
                if nome == bytes(list(clients.values())[i],"utf8"):
                    print("achei")
                    index = i
                    break
            if index != 99999:
                print(index)
                list(clients.keys())[index].send(mensagem)
            else:
                client.send(bytes("usuário não encontrado na sala. :/","utf8"))
            
                
            ##list(clients.keys())[list(clients.values()).index(nome)].send(bytes(nome + " escreveu privado: " + mensagem,"utf8"))
            ##list(clients.keys())[list(clients.values()).index(name)]
        elif msg == bytes("sair()","utf8"):
            client.close()
            del clients[client]
            broadcast(bytes("%s saiu da sala." % name, "utf8"))
            print(bytes("%s saiu da sala." % name, "utf8")) 
            break
        else:
            broadcast(msg, name+" escreveu: ")
            


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)

        
clients = {}
addresses = {}

HOST = ''
PORT = 33000
BUFSIZ = 448
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
