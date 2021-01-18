import socket
import sys
import errno

# input check
HOST = ''
try:
    PORT = int(sys.argv[1])
except IndexError:
    sys.exit("Please make sure you enter the port.")
if PORT < 1024:
    sys.exit("Please use a port between 1024 and 65535.")


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((HOST, PORT))
except OSError as e:
    if e.errno == errno.EADDRINUSE:
        sys.exit("This port is already in use. Try another one.")
    else:
        sys.exit("Unexpected error: {0}".format(e))

s.listen()
while True:
    conn, addr = s.accept()
    with conn:
        data = conn.recv(1024)
        if not data:
            break
        print("Receiving:", repr(data), file=sys.stdout)
        conn.sendall(data)
