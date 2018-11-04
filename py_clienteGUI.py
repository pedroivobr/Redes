#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
#from socket import AF_INET, socket, SOCK_STREAM
import socket
from threading import Thread
import tkinter
import time

def decodificar(msg_recebida):
    array = msg_recebida.slipt('/0')
    return array
def codificar(destino,nome,cmd,mensagem):
    protocolo = "{}/0{}/0{}/0{}/0{}/0{}".format((16 + len(mensagem)),ip_client,destino,nome,cmd,mensagem)
    return protocolo

ip_client = socket.gethostbyname(socket.gethostname())
ip_servidor = ""


def receive():
    """Essa função mantem o cliente recebendo dados do servidor."""
    while True:
        try:
            msg_servidor = client_socket.recv(BUFFERSIZE).decode("utf8")
            msg = decodificar(msg_servidor)
            msg_list.insert(tkinter.END, "%s escreveu: %s" %(msg[4],msg[-1]))
        except OSError:  # Possibly client has left the chat.
            break


def send(event=None):  # event is passed by binders.
    """A função é chamada quando for apertado o botão ENVIAR,
    para enviar a msg ao servidor."""
    msg = my_msg.get()
    my_msg.set("")  #limpa o campo de entrada

    if msg[0:7] == "privado":
        index = 99999           
        for i in range(len(msg)):
            if "," == chr(msg[i]):
                index = i
                break
        cmd = "privado"
        nick = msg[8:index]
        mensagem = msg[index + 1:-1]
    elif msg == "sair()":
        nick = "SERVIDOR"
        cmd = "sair"
        mensagem = "sair"
        client_socket.close()
        janela.destroy()
    elif msg == "listar()":
        nick = "SERVIDOR"
        cmd = "listar"
        mensagem = "listar()"
    else:
        nick = "SERVIDOR"
        cmd = "falar"
        mensagem = msg
    protocolo = codificar(ip_servidor,nick,cmd,mensagem)
    client_socket.send(bytes(protocolo, "utf8"))
    


def on_closing(event=None):
    """Essa função é chamada quando a janela for fechada (Xzinho)."""
    client_socket.send(bytes("sair()", "utf8"))
    client_socket.close()
    janela.destroy()


janela = tkinter.Tk()
janela.title("PY Chat :3")
janela["bg"] = "grey"

#LarguraxAltura+MargemEsq+MargemTop
#600x300x100x200
janela.geometry("600x450+100+200")

messages_frame = tkinter.Frame(janela)
my_msg = tkinter.StringVar()  #For the messages to be sent.
my_msg.set("Digite sua mensagem aqui.")
scrollbar = tkinter.Scrollbar(messages_frame)
msg_list = tkinter.Listbox(messages_frame, height=20, width=80, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()


entry_field = tkinter.Entry(janela , width=80,textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()

send_button = tkinter.Button(janela, width=12,text="Enviar", command=send)
send_button.pack()

janela.protocol("WM_DELETE_WINDOW", on_closing) ##caso a janela fechar

##conexão
HOST = "127.0.0.1"#input('Enter host: ')
PORT = "33000"#input('Enter port: ')
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

ip_servidor = HOST

BUFFERSIZE = 1024
ADDR = (HOST, PORT)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()

janela.mainloop()


