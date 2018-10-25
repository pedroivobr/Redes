import socket
import sys
import threading # threads

global soc
soc = 0

# define uma classe para a criacao de threads
class minhaThread (threading.Thread):
    # redefine a funcao __init__ para aceitar a passagem parametros de entrada
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.id = threadID
    # a funcao run() e executada por padrao por cada thread
    def run(self):
        if(self.id==0):
            entrada_teclado()
        elif(self.id==1):
            receber_servidor()



def entrada_teclado():
    print("iniciou thread 1")
    message = input(" -> ")

    while message != 'quit':
        soc.sendall(message.encode("utf8"))
        message = input(" -> ")


def receber_servidor():
    print("iniciou thread 2")
    while 1:
        printar = soc.recv(5120).decode("utf8")
        print(printar)



def main():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "127.0.0.1"
    port = 8888
    thread1 = minhaThread(0)
    thread2 = minhaThread(1)
    
    try:
        soc.connect((host, port))
    except:
        print("Connection error")
        sys.exit()

    print("Enter 'quit' to exit")

    
    thread1.start()
    thread2.start()

    soc.send(b'--quit--')

if __name__ == "__main__":
	main()
