import socket
HEADER = 64
PORT = 5050
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER =   socket.gethostbyname(socket.gethostname())



ADDR = (SERVER, PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
def send(msg:str):
    message = msg.encode(FORMAT)
    msgLength = len(message)
    sendLength = str(msgLength).encode(FORMAT)
    sendLength += b' ' * (HEADER - len(sendLength))
    client.send(sendLength)
    client.send(message)
    

while True:
    msg = input("Enter message: ")
    send(msg)
    print(client.recv(2048).decode(FORMAT))
    if msg == DISCONNECT_MESSAGE:
        break
    
   

    

    



    

    
    