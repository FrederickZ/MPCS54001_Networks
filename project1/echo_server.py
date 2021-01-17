import socket
import sys

HOST = ''  # HOST on this local server: linux.cs.uchicago.edu 
PORT = int(sys.argv[1])
if PORT < 1024:
    sys.exit("Please use a port between 1024 and 65535.")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print("Connected by", addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
