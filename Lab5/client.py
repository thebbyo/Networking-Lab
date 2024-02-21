import socket
import time

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

clSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servAddr = ('127.0.0.1', 8888)
clSocket.connect(servAddr)

headLen = 12
recBufSize = 4
mss = 20
winSize = mss
clSocket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, recBufSize)

seqNum = 0
expAckNum = 0

filename = "send.txt"
with open(filename, "rb") as file:
    data = file.read()
dataLen = len(data)
print(f"Length of the file {dataLen}")

timeout = 2
startTime = time.time()
recWin = 50
sentSize = 0
dupAck = 0
lastAck = 0

while seqNum < dataLen:
    currSentSize = 0
    while currSentSize < winSize and seqNum < dataLen:
        sendSize = min(mss, dataLen - seqNum)
        clSocket.sendall(makeHeader(seqNum, seqNum, 0, 0, 0) + data[seqNum:seqNum + sendSize])
        print(f"Data sent of sequence number {seqNum}")
        currSentSize += sendSize
        sentSize += sendSize
        seqNum += sendSize

    expAckNum = seqNum
    ackPkt = clSocket.recv(headLen)
    print("Acknowledgement packet received")
    seqNum, ackNum, ack, sf, recWin = fromHeader(ackPkt)
    print(f"Sequence number {seqNum}, Expected Acknowledgment Number {expAckNum}, Acknowledgment Number {ackNum}")
    winSize = min(2 * recBufSize, recWin)

    if ackNum == lastAck:
        dupAck += 1
    else:
        dupAck = 0
    if dupAck == 3:
        print("Received Triple Duplicate Acknowledgement, go back to last_ack")
        dupAck = 0
        seqNum = lastAck

    lastAck = ackNum

clSocket.close()
