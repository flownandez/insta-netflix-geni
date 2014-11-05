import socket   #for sockets
import sys  #for exit
 
# create dgram udp socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()
 
host = '10.10.2.2';
port = 8888;
msg = ""
msgNum = 1

while(1) :
    msg = str(msgNum) + " "
    while len(msg) < 1024 :
        msg = msg + "A"

    try :
        #Set the whole string
        s.sendto(str(msg), (host, port))
         
        # receive data from client (data, addr)
        d = s.recvfrom(1024)
        reply = d[0]
        addr = d[1]
         
        print 'Server reply : ' + reply
        msgNum = msgNum + 1
     
    except socket.error, msg:
        print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()
