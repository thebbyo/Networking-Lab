#interacts with the server3

import socket
HEADER = 64
PORT = 5050
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER =   socket.gethostbyname(socket.gethostname())



ADDR = (SERVER, PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
def send(id:str, password:str, choice:str = "", amount:str = ""):
    msg = id + password + choice+ amount
    message = msg.encode(FORMAT)
    msgLength = len(message)
    sendLength = str(msgLength).encode(FORMAT)
    sendLength += b' ' * (HEADER - len(sendLength))
    client.send(sendLength)
    client.send(message)

while True:
    id = input("Enter ID: ")
    password = input("Enter Password: ")
    send(id, password)

  
    response = client.recv(2048).decode(FORMAT)
    if response == "Invalid ID or Password\n":
        print(response)
        continue

    print(response)

    choice = input("Enter choice: ")
    send(id, password, choice)

    if choice == "1":
        print(client.recv(2048).decode(FORMAT))
    
    elif choice == "2":
        print(client.recv(2048).decode(FORMAT))
        amount = input("Enter amount: ")
        send(id, password, amount)
        print(client.recv(2048).decode(FORMAT))

    elif choice == "3":
        print(client.recv(2048).decode(FORMAT))
        amount = input("Enter amount: ")
        send(id, password, amount)
        print(client.recv(2048).decode(FORMAT))

   

    

    



    

    
    