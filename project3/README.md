# Project 3
### Frederick Y. Zhu (yumingz; 12244682)

## Usage
1. Start the `pingservar.jar` first by java
   * Please use `127.0.0.1` as host input. I hardcoded it to forbidden the use of `localhost` as it does not work for me.
   * Please make sure your input is correct, especially the identical port input you used in both command as I am not able to check the connection beforehand for the reason of my ignorance of `pingserver`. The project does only input volume and type check.

2. Use `python ping_client.py <inputs>` following the **no-option-name convention**
   * For example:
     ```zsh
     python3 ping_client.py 127.0.0.1 56789 10 100 6000
     ``` 

3. Testing by moderating inputs. This program should be fully functional

4. Please wait for the analysis. It should be printed out after the `python` project exits, the time of which is based on your TIMEOUT input.
   * If encountering packet loss, in practice the client will not know the packet is lost until the end of the process because the server does not send a loss message. Hence, the best practice should be an after-process printout.
   * For the same reason, the `time elapsed` analysis follows these conditions:
     1. If all packets received, no matter they are all correct or not, `time elapsed` is counted as the time last packet is received (not necessarily the last packet sent) minus the time the process starts
        ```
        $ java -jar pingserver.jar --port=56789 --loss_rate=0.0 --bit_error_rate=0.5 --avg_delay=500
        ```
        ```
        $ python3 ping_client.py 127.0.0.1 56789 10 100 6000
        NOTICE! Statistics will be printed out AFTER TIMEOUT.

        PING 127.0.0.1
        PONG 127.0.0.1: seq=4 time=329ms
        PONG 127.0.0.1: seq=3 time=572ms
        Checksum verification failed for echo reply seqno=1
        PONG 127.0.0.1: seq=2 time=748ms
        Checksum verification failed for echo reply seqno=5
        Checksum verification failed for echo reply seqno=6
        Checksum verification failed for echo reply seqno=9
        Checksum verification failed for echo reply seqno=10
        PONG 127.0.0.1: seq=8 time=600ms
        Checksum verification failed for echo reply seqno=7

        --- 127.0.0.1 ping statistics ---
        10 transmitted, 4 received 60% loss, time 1320ms 
        rtt min/avg/max = 329/748/562
        ```
     2. If there is a packet loss, `time elapsed` is counted as the time the process encounters `socket.timeout` error minus the time the process starts (there will be a 'TIMEOUT' stamp as indication).
        ```
        $ java -jar pingserver.jar --port=56789 --loss_rate=0.5 --bit_error_rate=0.5 --avg_delay=500
        ```
        ```
        $ python3 ping_client.py 127.0.0.1 56789 10 100 6000
        NOTICE! Statistics will be printed out AFTER TIMEOUT.

        PING 127.0.0.1
        Checksum verification failed for echo reply seqno=4
        PONG 127.0.0.1: seq=7 time=77ms
        PONG 127.0.0.1: seq=10 time=575ms
        Checksum verification failed for echo reply seqno=8

        --- 127.0.0.1 ping statistics ---
        10 transmitted, 2 received 80% loss, time 7537ms (TIMEOUT)
        rtt min/avg/max = 77/575/325
        ``` 









