import socket   #for sockets
import sys  #for exit
 
# create dgram udp socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()
 
host = '10.10.3.2'
port = 8887
msg = ""
msgNum = 2

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
        replytmp = reply.split()
         
        print 'Server reply : ' + replytmp[0]
        msgNum = msgNum + 4
     
    except socket.error, msg:
        print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()
