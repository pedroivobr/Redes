#!/usr/bin/env python3
import socket
from threading import Thread

destino = ''
ip_servidor = socket.gethostbyname(socket.gethostname())

def decodifidar(msg_recebida):
    array = msg_recebida.slipt('/0')
    return array
def codificar(destino,nome,cmd,mensagem):
    protocolo = "{}/0{}/0{}/0{}/0{}/0{}".format((16 + len(msg)),ip_servidor,destino,nome,cmd,mensagem)
    return protocolo

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s foi conectado." % client_address)
        client.send(bytes(codificar(client_address[0],"usuarioX","listar","Bem-vindo ao PyChat!!!!!! Agora coloque um nickname no campo e aperte ENTER!"),"utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    nome =''
    mensagem=''

    name = decodificar(client.recv(BUFSIZ))
    name = name[-1]
    welcome = 'Bem-vindo %s! Digite comandos() para mais informações.' % name
    client.send(bytes(codificar(client_address[0],name,"listar",welcome),"utf8"))
    msg = "%s enctrou no chat!" % name
    broadcast("falar",msg)
    clients[client] = name

    while True:
        msg = decodificar(client.recv(BUFSIZ))
        print(msg)
        if msg[4] == "listar":
            client.send(bytes(codificar(client_address[0],name,"listar","Lista de usuários:"),"utf8"))
            for i,v in clients.items():
                mensagem = "<" + str(v) +", "+str(i.getpeername()[0]) + ", " + str(i.getpeername()[1]) + ">"
                client.send(bytes(codificar(client_address[0],name,"listar",mensagem),"utf8"))
            #client.send(bytes(msg,"utf8"))
        elif msg[4] == "nome":
            clients[client] = msg[-1][5:-1]
            broadcast("%s alterou o nome para %s." %(name,msg[-1][5:-1]), "utf8")
            name = msg[-1][5:-1]
        elif msg[4] == "privado":
            index = 99999           
            for i in range(len(msg)):
                if "," == chr(msg[i]):
                    index = i
                    break
            nome = msg[8:index]
            mensagem = "PRIVADO[" + nome + "]:" + msg[index + 1:-1]
            for i in range(len(clients)):
                if nome == bytes(list(clients.values())[i],"utf8"):
                    print("achei")
                    index = i
                    break
            if index != 99999:
                print(index)
                list(clients.keys())[index].send(bytes(codificar(client_address[0],name,"comandos",mensagem),"utf8"))
            else:
                msg = "usuário não encontrado na sala. :/"
                client.send(bytes(codificar(client_address[0],name,"comandos",msg),"utf8"))
        elif msg[4] == "sair":
            client.close()
            del clients[client]
            msg = "%s saiu da sala." % name
            broadcast("sair",msg)
            print(bytes("%s saiu da sala." % name, "utf8")) 
            break
        elif msg[4] == "comados":
            msg = "lista de comandos:\n\nlistar() - para listar usuários conectados.\n\nprivado(usuario,mensagem) - para enviar uma MENSAGEM privada para um USUARIO.\n\nsair()- para sair para finalizar o cliente.\n\nnome(nick_novo) - para alterar o nickname."
            client.send(bytes(codificar(client_address[0],name,"comandos",msg),"utf8"))
        else:
            msg = "%s escreveu: %s"%(name,msg[-1])
            broadcast("falar",msg)
            


def broadcast(cmd,msg):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock,i in clients.items():
        sock.send(bytes(codificar(sock.getpeername()[0],str(i),cmd,msg),"utf8"))

        
clients = {}
addresses = {}

HOST = ''
PORT = 33000
BUFSIZ = 448
ADDR = (HOST, PORT)

SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
