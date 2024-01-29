# (a) 2. Capital letter to Small letter conversion for a line of text
# ii. Send an integer and operation name (either ‘prime’ or ‘palindrome’) to the server and
# check whether it’s a prime (or palindrome) or not . This problem interacts with client and server 2.

import socket
import threading 
import utils

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECTMESSAGE = "!DISCONNECT"

SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

print (SERVER)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handleClient(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msgLength = conn.recv(HEADER).decode(FORMAT)
        if msgLength:
            msgLength = int(msgLength)
            msg = conn.recv(msgLength).decode(FORMAT)
            if msg == DISCONNECTMESSAGE:
                connected = False

            isPalidrome = utils.isPalidrome(msg)

            msg = int(msg)


            response = f"[Prime] {utils.isPrime(msg)} [Palidrome] {isPalidrome}"

            conn.send(response.encode(FORMAT))

            
            
    conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handleClient, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")

start()
