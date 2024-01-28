import socket
import threading
import utils

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECTMESSAGE = "!DISCONNECT"

SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

print(SERVER)

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
                break
            name = utils.getName(int(msg[0]), int(msg[1:5]))

            str = f"Welcome {name}!\n"
            str += "1. Check Balance\n"
            str += "2. Deposit\n"
            str += "3. Withdraw\n"
            str += "4. Exit\n"
            conn.send(str.encode(FORMAT))

            msgLength = conn.recv(HEADER).decode(FORMAT)
            if msgLength:
                msgLength = int(msgLength)
                msg = conn.recv(msgLength).decode(FORMAT)

                if msg == DISCONNECTMESSAGE:
                    break

                if msg[5] == "1":
                    str = f"Your balance is {utils.getBalance(int(msg[0]), int(msg[1:5]))}\n"
                    conn.send(str.encode(FORMAT))

                elif msg[5] == "2":
                    str = "Enter amount to deposit: "
                    
                    conn.send(str.encode(FORMAT))
                    msgLength = conn.recv(HEADER).decode(FORMAT)
                    if msgLength:
                        msgLength = int(msgLength)
                        msg = conn.recv(msgLength).decode(FORMAT)

                        if msg == DISCONNECTMESSAGE:
                            break
                        utils.deposit(int(msg[0]), int(msg[1:5]), int(msg[5:]))
                        str = f"Your balance is {utils.getBalance(int(msg[0]), int(msg[1:5]))}\n"
                        conn.send(str.encode(FORMAT))

                elif msg[5] == "3":
                    str = "Enter amount to withdraw: "
                    
                    conn.send(str.encode(FORMAT))
                    msgLength = conn.recv(HEADER).decode(FORMAT)
                    if msgLength:
                        msgLength = int(msgLength)
                        msg = conn.recv(msgLength).decode(FORMAT)

                        if msg == DISCONNECTMESSAGE:
                            break
                        utils.withdraw(int(msg[0]), int(msg[1:5]), int(msg[5:]))
                        str = f"Your balance is {utils.getBalance(int(msg[0]), int(msg[1:5]))}\n"
                        conn.send(str.encode(FORMAT))

                elif msg[5] == "4":
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
