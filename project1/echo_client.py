import socket
import sys

# input check
try:
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
except IndexError:
    sys.exit("Please make sure you enter both host and port.")
if HOST != "linux.cs.uchicago.edu":
    print("WARNING: You are not on the supported host.")

# connection test
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        print("Testing connection...")
        s.connect((HOST, PORT))
        test = "test connection".encode('ascii')
        s.sendall(test)
        data = s.recv(1024)
        if data:
            print("Connection test success.")
        else:
            sys.exit("Connection test failed.")
    except ConnectionRefusedError:
        sys.exit("Invalid port.")
    except socket.gaierror:
        sys.exit("Invalid host.")


while True:
    for line in sys.stdin:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            byte_msg = line.encode('ascii')
            s.sendall(byte_msg)
            data = s.recv(1024)
            print('Received:', repr(data), file=sys.stdout)
    
    

