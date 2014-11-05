import socket
import sys
import time
 
HOST = '10.10.7.2'   # Symbolic name meaning all available interfaces
PORT = 8890 # Arbitrary non-privileged port
 
# Datagram (udp) socket
try :
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print 'Socket created'
except socket.error, msg :
    print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
 
 
# Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
 
firstround = 1
file = open("datalog", "w")
#now keep talking with the client
while 1:
    # receive data from client (data, addr)
    d = s.recvfrom(1024)
    data = d[0]
    addr = d[1]
     
    if not data: 
        break
     
    reply = 'OK...' + data
    logdata = data.split()

    if firstround == 1 :
        startime = time.time()
        firstround = 0
        file.write(str(startime) + ' ' + logdata[0] + '\n')
    else :
        recevtime = time.time()
        transtime = startime - recevtime
        file.write(str(transtime) + ' ' + logdata[0] + '\n')
     
    s.sendto(reply , addr)
    print 'Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + data.strip()
     
    if int(logdata[0]) > 500 :
        file.close()
        break
s.close()
