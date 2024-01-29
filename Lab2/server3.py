# i. Design and describe an application-level protocol to be used between an automatic teller
# machine and a bank’s centralized server. Your protocol should allow a user’s card and
# password to be verified, the account balance (which is maintained at the centralized
# computer) to be queried, and an account withdrawal to be made (that is, money
# disbursed to the user). Your protocol entities should be able to handle the all-too-common
# cases in which there is not enough money in the account to cover the withdrawal. Specify
# your protocol by listing the messages exchanged and the action taken by the automatic
# teller machine or the bank’s centralized computer on transmission and receipt of
# messages. Sketch the operation of your protocol for the case of a simple withdrawal with
# no errors.
# ii. HOME WORK – Enhance the above protocol so that it can handle errors related to both
# request and response messages to and from the server.


import socket
import threading
import utils
import random

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
            if utils.getName(int(msg[0]), int(msg[1:5])) == False:
                str = "Invalid ID or Password\n"
                conn.send(str.encode(FORMAT))
                continue
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
                    rand = random.randint(0, 10)
                    str = "Enter amount to deposit: "
                    
                    conn.send(str.encode(FORMAT))
                    msgLength = conn.recv(HEADER).decode(FORMAT)
                    if msgLength:
                        msgLength = int(msgLength)
                        msg = conn.recv(msgLength).decode(FORMAT)

                        if msg == DISCONNECTMESSAGE:
                            break
                        if rand > 5:
                            utils.deposit(int(msg[0]), int(msg[1:5]), int(msg[5:]))
                            str = f"Your balance is {utils.getBalance(int(msg[0]), int(msg[1:5]))}\n"
                            conn.send(str.encode(FORMAT))

                        else:
                            str = "Transaction failed\n"
                            str+= f"Your balance is {utils.getBalance(int(msg[0]), int(msg[1:5]))}\n"
                            str+= "Please try again\n"
                            conn.send(str.encode(FORMAT))
                        

                elif msg[5] == "3":
                    str = "Enter amount to withdraw: "
                    rand = random.randint(0, 10)
                    
                    conn.send(str.encode(FORMAT))
                    msgLength = conn.recv(HEADER).decode(FORMAT)
                    if msgLength:
                        msgLength = int(msgLength)
                        msg = conn.recv(msgLength).decode(FORMAT)

                        if msg == DISCONNECTMESSAGE:
                            break
                        if rand > 5:
                            utils.withdraw(int(msg[0]), int(msg[1:5]), int(msg[5:]))
                            str = f"Your balance is {utils.getBalance(int(msg[0]), int(msg[1:5]))}\n"
                            conn.send(str.encode(FORMAT))
                        
                        else:
                            str = "Transaction failed\n"
                            str+= f"Your balance is {utils.getBalance(int(msg[0]), int(msg[1:5]))}\n"
                            str+= "Please try again\n"
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
