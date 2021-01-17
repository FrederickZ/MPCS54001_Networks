import socket
import sys

HOST = sys.argv[1]
PORT = int(sys.argv[2])

if HOST != "linux.cs.uchicago.edu":
    print("WARNING: You are not on the supported host.")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.connect((HOST, PORT))
        s.sendall(b"Hello, world!")
        data = s.recv(1024)
        print('Received', repr(data))
    except ConnectionRefusedError:
        print("Invalid port.")
    except socket.gaierror:
        print("Invalid host.")
    
    
    

