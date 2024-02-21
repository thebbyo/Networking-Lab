import os
import socket
import threading
import struct

IP = '127.0.0.1'
PORT = 4490
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"
dic={}

def read_dns_records(file_path):
    records = {}

    with open(file_path, 'r') as file:
        for line in file:
            parts = line.split()
            name = parts[0]
            value = parts[1]
            type = parts[2]
            records[name] = {'value': value, 'type': type}

    return records

# Usage
dns_records = read_dns_records('dns_records.txt')

def handle_client(data, addr, server):
    print(f"[RECEIVED MESSAGE] {data} from {addr}.")
    data = data.split()
    print(data[0])
    print(data[1])

    # Parse the DNS query
    query_type = data[1]
    domain_name = data[0][4:]  # Remove "QRY:" from the domain name

    # Check if the query matches any DNS records
    if domain_name in dns_records:
        record = dns_records[domain_name]

        # Construct a DNS response
        response = f"RES:{domain_name}:{record}"
        server.sendto(response.encode('utf-8'), addr)
    else:
        # Handle the case when no match is found
        error_response = "RES:Error:Domain not found"
        server.sendto(error_response.encode('utf-8'), addr)
def main():
   
    print("[STARTING] Server is starting")
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(ADDR)
    print(f"[LISTENING] Server is listening on {IP}:{PORT}.")

    while True:
        data, addr = server.recvfrom(SIZE)
        data = data.decode(FORMAT)
        thread = threading.Thread(target=handle_client, args=(data, addr,server))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    main()