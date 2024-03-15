
import socket
import time
def trans_layer_decode(packet):
    seq=packet[:6]
    ack=packet[6:12]
    win=packet[12:16]
    check=packet[16:20]
    return (int(seq.decode('utf-8')),int(ack.decode('utf-8')),int(win.decode('utf-8')),int(check.decode('utf-8')))
def make_packet(seq,ack,window,checksum):
    transport_header = f'{seq:06d}{ack:06d}{window:04d}{checksum:04d}'.encode('utf-8')[:20].ljust(20)
    
    network_header = b'\x45\x00\x05\xdc'  
    network_header += b'\x00\x00\x00\x00'  
    network_header += b'\x40\x06\x00\x00'  
    network_header += b'\x0a\x00\x00\x02'  
    network_header += b'\x0a\x00\x00\x01'  
    
    
    packet = network_header + transport_header
    return packet
rcvtim=1
mss=1460
max_rcv=1

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8882))
client_socket.settimeout(4)

print('Connected to server')


max_buffer_size = 1465*50  
data_buffer = b''
curr_buffer_size=0
total_received = 0
start_time = time.time()
tot_time=start_time
try:
    
    with open('received_file.txt', 'wb') as file:
        expected_sequence_number = 0
        while True:
            start_time = time.time()
            curr_rcv=0
            while max_rcv>curr_rcv:

                try:
                    packet = client_socket.recv(1500)
                except socket.timeout:
                    print('No data received within 5 seconds')
                    continue

                curr_rcv+=1
                if not packet:
                    break
                network_header = packet[:20]
                transport_header = packet[20:40]
                payload = packet[40:]
                payload_size=len(payload)
                actual_payload = payload[:payload_size]
                expected_sequence_number += payload_size 

                sequence_number,ack,max_rcv,checksum=trans_layer_decode(transport_header)
                data_buffer += payload
                total_received += len(payload)
                print(sequence_number,ack,max_rcv,checksum)
               
            
            
            if curr_rcv!=0:
                rwnd=int((max_buffer_size-len(data_buffer))/mss)
                checksum=45
                packet = make_packet(total_received,sequence_number+payload_size,rwnd,checksum)
                print('ack send')
                client_socket.send(packet)

                file.write(data_buffer)
                data_buffer = b''
                print({total_received})
                start_time = time.time()
            else:
                packet = make_packet(total_received,sequence_number+payload_size,rwnd,checksum)
                print('ack send')
                client_socket.send(packet)

                break
        if data_buffer:
                file.write(data_buffer)
        client_socket.close()
        print('Done' )
        print(time.time()-tot_time)
except :
    client_socket.close()
    print('Done' )
    print(time.time()-tot_time)