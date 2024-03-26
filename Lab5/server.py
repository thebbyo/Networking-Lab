import socket
import time
import random

def makeHeader(seqNum=0, ackNum=0, ack=0, sf=0, rwnd=0):
    header = seqNum.to_bytes(4, byteorder="little")
    header += ackNum.to_bytes(4, byteorder="little")
    header += ack.to_bytes(1, byteorder="little")
    header += sf.to_bytes(1, byteorder="little")
    header += rwnd.to_bytes(2, byteorder="little")
    return header

def fromHeader(segment):
    seqNum = int.from_bytes(segment[:4], byteorder="little")
    ackNum = int.from_bytes(segment[4:8], byteorder="little")
    ack = int.from_bytes(segment[8:9], byteorder="little")
    sf = int.from_bytes(segment[9:10], byteorder="little")
    rwnd = int.from_bytes(segment[10:12], byteorder="little")
    return seqNum, ackNum, ack, sf, rwnd

servSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servAddr = ('', 8888)
servSock.bind(servAddr)
servSock.listen(1)

clSocket, clientAddress = servSock.accept()
print(f"Accepted connection from {clientAddress}")

recBufSize = 16
winSize = 4 * recBufSize
mss = 20
clSocket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, recBufSize)

expectedSeqNum = 0
ackNum = 0
startTime = time.time()
clSocket.settimeout(1)
timeout = 1
receivedData = b''
bufferData = b''

while True:
    try:
        header = clSocket.recv(12)
        seqNum, ackNum, ack, sf, rwnd = fromHeader(header)
        print(f"Sequence number from client {seqNum}, Acknowledgement from client {ackNum}")
        data = clSocket.recv(mss)
        print(data)
        print("Header & data received")

    except:
        print("Exception block encountered")
        rwind = recBufSize - (len(bufferData) + mss - 1) // mss
        toSendAck = makeHeader(expectedSeqNum, ackNum, 1, 0, rwind)
        print(f"Sequence number {seqNum}, Acknowledgement number {ackNum}")
        clSocket.sendall(toSendAck)
   
   
   
   
   
   
   
        startTime = time.time()
        continue

    if not data:
        print("No data received")
        break

    seqNum = ackNum

    if seqNum == expectedSeqNum and random.randint(0, 2) != 0:
        bufferData += data
        ackNum += len(data)
        expectedSeqNum += len(data)
        toSendAck = makeHeader(seqNum, ackNum, 1, 0, 8)
        if len(bufferData) >= recBufSize:
            receivedData += bufferData
            bufferData = b''
            try:
                clSocket.sendall(toSendAck)
                print(f"Sequence number {seqNum}, Acknowledgement number {ackNum}")
            except:
                print("Client closed")
    else:
        toSendAck = makeHeader(expectedSeqNum, expectedSeqNum, 1, 0, 0)
        clSocket.sendall(toSendAck)
        clSocket.sendall(toSendAck)
        clSocket.sendall(toSendAck)
        print(f"Sequence number {seqNum}, Acknowledgement number {ackNum}")

# Write received data to a file
with open("received_data.txt", "wb") as file:
    file.write(receivedData)

clSocket.close()
servSock.close()
