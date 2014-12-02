import socket   #for sockets
import sys  #for exit
 
# create dgram udp socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()
 
host = '10.10.1.2'
port = 8887
msg = ""
msgNum = 0
tokens = [0, 0]
reply = ""
while(1) :
    msg = str(msgNum) + " 1 "
    while len(msg) < 1024 :
        msg = msg + "A"

    try :
		#Set the whole string
		s.sendto(str(msg), (host, port))
		
		# receive data from client (data, addr)
		d = s.recvfrom(1024)
		
		reply2 = reply;		
		reply = d[0]
		addr = d[1]
		replytmp = reply.split()
		print 'Server reply : ' + reply
	
		if reply != reply2 :
			totalTokens = int(replytmp[0]);
			tokens[0] = int(replytmp[1]);
			startingPkt = int(replytmp[(replytmp.index("X") + 1)])

		currentToken = tokens[0]; 
		msgNum = startingPkt + currentToken;
		if currentToken == tokens[0] : 
			tokens[0] = tokens[0] + totalTokens;
			#else tokens[1] = tokens[1] + totalTokens; 

     
    except socket.error, msg:
        print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()
