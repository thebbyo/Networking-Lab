import os
import socket
import time

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostbyname(socket.gethostname())
format = "utf-8"

try:
    my_socket.connect((host, 5005))
    print("Connected to the server...")
except Exception as e:
    print(f"Connection failed: {e}")
    exit(0)

filename = my_socket.recv(1024).decode(format)
filesize = my_socket.recv(1024).decode(format)

str = f"File {filename} of size {filesize} bytes is being received. Do you want to continue? (y/n): "
choice = input(str)
my_socket.send(choice.encode(format))
if choice == "n":
    exit(0)


with open("./received_" + filename, 'wb') as file:

    c = 0
    starttime = time.time()

    while c < int(filesize):
        data = my_socket.recv(1024)
        c += len(data)
        file.write(data)
        print(f"Received {c} bytes")

    endtime = time.time()
    print(f"Time taken to receive the file: {endtime - starttime} seconds")

my_socket.close()
exit(0)
