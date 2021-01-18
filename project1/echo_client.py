import socket
import sys

try:
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
except IndexError:
    sys.exit("Please make sure you enter both host and port.")

if HOST != "linux.cs.uchicago.edu":
    print("WARNING: You are not on the supported host.")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.connect((HOST, PORT))
        for line in sys.stdin:
            byte_msg = line.encode('ascii')
            s.sendall(byte_msg)
            data = s.recv(1024)
            print('Received:', repr(data))
        
    except ConnectionRefusedError:
        print("Invalid port.")
    except socket.gaierror:
        print("Invalid host.")
    
    
    

