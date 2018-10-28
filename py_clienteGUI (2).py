#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter


def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFFERSIZE).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:  # Possibly client has left the chat.
            break


def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        janela.quit()


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    send()


janela = tkinter.Tk()
janela.title("PY Chat :3")
janela["bg"] = "grey"

#LarguraxAltura+MargemEsq+MargemTop
#600x300x100x200
janela.geometry("600x450+100+200")

#Label(janela, text="OI =D").pack()

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
HOST = input('Enter host: ')
PORT = input('Enter port: ')
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFFERSIZE = 448
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()

janela.mainloop()


