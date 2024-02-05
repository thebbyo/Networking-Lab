import socket
import os
import time
import threading


HEADER = 64
PORT = 5005
FORMAT = 'utf-8'
DISCONNECTMESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handleClient(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True

    while connected:
        fileName = input("Enter the name: ")
        conn.send(fileName.encode(FORMAT))
        fileSize = os.path.getsize(fileName)

        conn.send(str(fileSize).encode(FORMAT))
        choice = conn.recv(1024).decode(FORMAT)
        if choice == "n":
            print("File transfer cancelled")
            conn.send(DISCONNECTMESSAGE.encode(FORMAT))
            conn.close()
            print(f"[DISCONNECTED] {addr} has been disconnected")
            break
        time.sleep(1)
        print(f"[SENDING] Sending {fileName} to {addr}")
        with open(fileName, "rb") as f:
            start = time.time()
            bytesToSend = f.read(1024)
            conn.send(bytesToSend)
            while bytesToSend != "":
                bytesToSend = f.read(1024)
                conn.send(bytesToSend)
            end = time.time()

        print(f"time taken to send the file: {end - start} seconds")

        print(f"[SENT] {fileName} has been sent")
        connected = False
        conn.send(DISCONNECTMESSAGE.encode(FORMAT))
        conn.close()
        print(f"[DISCONNECTED] {addr} has been disconnected")
        break

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
