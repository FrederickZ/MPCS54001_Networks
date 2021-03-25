# Project 2: UDP-Based TFTP Server
### Frederick Y. Zhu
This project creates a tftp server on a certain port. User can call `tftp` in terminal as client and interact with the 
server. 

## Usages
Following instructions shows how to use this server that is safe even in the case when user start `tftp_server.py` and 
`tftp` on the same repository. However, I strongly recommand user to start `tftp` client in a different repository than 
`tftp_server.py`.

### Step 1: start `tftp_server.py`
```
$ python3 tftp_server.py <port> <timeout>
```
This server will handle almost all the input errors and connection errors. Follow the error messages if needed.

### Step 2: start `tftp`
```
$ tftp
tftp > connect 127.0.0.1 <port>
tftp > binary
tftp > verbose
Verbose mode on.
```
Two notes here:
1. use the port that you proceeds in step 1;
2. `localhost` does not work for me; you may try if you want.

### After running the tests
For `tftp`, simply use `quit` command to exit. However for `tftp_server.py`, please use KeyboardInterrupt twice to kill 
the program because of the naive multi-threading.

## Tests
### Example 1:
```
tftp> get file.txt newfile.txt
```
This will download `file.txt` from server directory to client directory as `newfile.txt`. Error pops if there is no 
`file.txt`. However, no error would pop if you already have `newfile.txt`; new contents will be appended. (This is the 
nature of `tftp`, which we are not able to control.)

### Example 2:
```
tftp> put newfile.txt myfile.txt
```
Server will send an error packet to the client if the written file exists so it is impossible to put a file without 
renaming it if the program is conducted under one directory (that is why I recommend separate server and client out). 

## Important !!!
I tried `java` but failed. I have no time to put it on Ed Discussion. However, I handled duplicate ACK and DATA pack in 
the script, and I think it is the problem of `tftp`. Here is my reasoning.

```
Received WRQ from client
Forwarded WRQ to server

Received ACK 3
Forwarded ACK 3
Received DATA 4
Forwarded DATA 4
Received ACK 4
Forwarded ACK 4
Received DATA 5
Dropped DATA 5
Received ACK 4
Forwarded ACK 4
Received ACK 4
Forwarded ACK 4

```
Here I use `put` in `tftp` and clearly `DATA 5` is dropped by random. After `tftp` sent `DATA 5` to `8081`, which is 
that JAVA port, server continue sent `ACK 4` because it had not received `DATA 5`, and clearly `8081` forwarded 
`ACK 4`. However, `8081` never received any packets from the client after that. It is very weired. You may try that out 
or I may come to one of the office hour to discuss about it.



## References
### General References (provided by the instruction)
* https://tools.ietf.org/html/rfc1350
* http://www.tcpipguide.com/free/t_TrivialFileTransferProtocolTFTP.htm

### Other References
* https://realpython.com/intro-to-python-threading/
* https://smitsgit.github.io/blog/html/2018/06/13/tftp.html
* https://www.programmersought.com/article/40282700305/
* https://github.com/cizixs/tftp/blob/master/tftp/tftp_client.py