import socket
import os
import sys
import errno
import struct
import time
from threading import Thread

# UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# input check
try:
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    COUNT = int(sys.argv[3])
    PERIOD = int(sys.argv[4]) / 1000
    TIMEOUT = int(sys.argv[5]) / 1000
except IndexError:
    sys.exit("Please make sure you have five inputs.")
except ValueError:
    sys.exit("Please make sure your input types are correct.")    

# connection check
# assume connection is stable

def pack(type, pid, seq):
    """
     1 byte 1 byte   2 bytes    2 bytes    2 bytes   6 bytes
    -----------------------------------------------------------
    | type | code | checksum | identifier | seq # | timestamp |
    -----------------------------------------------------------
    """
    timestamp = int(time.time() * 1000)
    packet = (struct.pack('!BBHHH', 8, 0, 0, pid, seq) + 
              struct.pack('!Q', timestamp)[2:])
    checksum = get_checksum([packet[2*i:2*(i+1)] for i in range(7)])
    packet = (struct.pack('!BBHHH', 8, 0, checksum, pid, seq) + 
              struct.pack('!Q', timestamp)[2:])
    return packet

def unpack(packet):
    packet_checksum, pid, seq = struct.unpack('!BBHHH', packet[0:8])[2:]
    timestamp = struct.unpack('!Q', b'\x00\x00' + packet[8:])[0]
    test_packet = (struct.pack('!BBHHH', 0, 0, 0, pid, seq) + 
                   struct.pack('!Q', timestamp)[2:])
    correct_checksum = get_checksum([test_packet[2*i:2*(i+1)] for i in range(7)])
    correct = (correct_checksum == packet_checksum)
    return seq, correct

def get_checksum(hex_list):
    checksum = 0
    for hex in hex_list:
        n = struct.unpack('!H', hex)[0]
        checksum += n
    checksum = 0xffff - ((0x0000ffff & checksum) + (checksum >> 16))
    return checksum

def get_analysis(log):
    n = 0
    nr = 0
    rttmin = (TIMEOUT + 1) * 1000 
    rttmax = -1
    rttsum = -1
    tmax = -1

    for i in range(COUNT):
        if (log['packets'][i]['correct'] == 1):
            n += 1
            rtt = log['packets'][i]['rtt']
            rttsum += rtt
            rttmin = min(rttmin, rtt)
            rttmax = max(rttmax, rtt)
            tmax = max(tmax, log['packets'][i]['received'])
        elif log['packets'][i]['received'] != 0:
            nr += 1
    nr += n
    pct = int((COUNT - n) / COUNT * 100)
    rttavg = int(rttsum / n)
    return n, nr, pct, rttmin, rttmax, rttavg, tmax

def listen_packets():
    global log
    while True:
        try:
            packet, addr = s.recvfrom(1024)
            t = time.time()
            seq, correct = unpack(packet)
            log['packets'][seq-1]['received'] = t
            log['packets'][seq-1]['rtt'] = int((t - log['packets'][seq-1]['sent']) * 1000)
            log['packets'][seq-1]['correct'] = correct
            if correct:
                print(f'PONG {addr[0]}: ' + 'seq={} time={}ms'.format(seq, log['packets'][seq-1]['rtt']))
            else:
                print(f"Checksum verification failed for echo reply seqno={seq}")
        except socket.timeout:
            t = time.time()
            n, nr, pct, rttmin, rttmax, rttavg, tmax = get_analysis(log)
            if nr != COUNT:
                timeout_msg = "(TIMEOUT)"
                tmax = t
            else:
                timeout_msg = ""
            log['end'] = tmax
            elapse = int((log['end'] - log['start']) * 1000)
            print('')
            print(f"--- {HOST} ping statistics ---")
            print(f"{COUNT} transmitted, {n} received {pct}% loss, time {elapse}ms " + timeout_msg)
            print(f"rtt min/avg/max = {rttmin}/{rttmax}/{rttavg}")
            sys.exit()

s.settimeout(TIMEOUT)
packet_listening_thread = Thread(target=listen_packets)
packet_listening_thread.start()
print("NOTICE! Statistics will be printed out AFTER TIMEOUT.")
print("")
print(f'PING {HOST}')
log = {
    'pid': os.getpid() % 65536,
    'packets': [],
    'start': time.time(),
    'end': -1
}
for i in range(COUNT):
    sent = s.sendto(pack(8, log['pid'], i+1), (HOST, PORT))
    log['packets'].append({
        'seq': i+1,
        'sent': time.time(),
        'received': 0,
        'rtt': -1,
        'correct': -1
    })
    if i != COUNT - 1:
        time.sleep(PERIOD)
