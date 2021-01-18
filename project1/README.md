# Project 1
### Frederick Y. Zhu (yumingz; 12244682)
This project creates an echo server and client on a network. Beyond instructions, several features implemented:
* Error/Exception handler:
    * Host and port input checking
        * Missing input (`IndexError`)
        * Server: Port range 1024 - 65535 (condition check)
        * Server: Port already in use (`OSError: [Errno 98]`)
        * Client: Not "linux.cs.uchicago.edu" (condition check) -> print a warning
    * Connection test: \
      Client runs a connection test before service runs, and it fails when:
        * Invalid host (`socket.gaierror`)
        * Invalid port (`ConnectionRefusedError`)
        * If host is not "linux.cs.uchicago.edu" and port is valid (80) -> test suspended
        * All other unknown cases, client exit with `Connection test failed.`
      
      If test is passed, server displays `Receiving: b'test connection'` and client displays `Connection test success.`




## Notes
### TCP Sockets
The sequence of socket API calls and the data flow for TCP:
![Data Flow for TCP](https://files.realpython.com/media/sockets-tcp-flow.1da426797e37.jpg)

## References
### General References (provided by the instruction)
* https://docs.python.org/3/howto/sockets.html
* https://docs.python.org/3/library/threading.html

### Other References
* https://realpython.com/python-sockets/
* https://www.geeksforgeeks.org/socket-programming-python/