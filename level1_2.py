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
tokens = [0, 0]
reply = ""
while(1) :
    msg = str(msgNum) + " 2 "
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
		index = reply.index("B")
		replytmp = reply.split()
		print 'Server reply : ' + reply + ' INDEX: ' + index
		print 'Server replytmp : ' + replytmp[index + 1] + " " + replytmp[index + 2]
	
		if reply != reply2 :
			totalTokens = int(replytmp[index + 1]);
			tokens[0] = int(replytmp[index + 2]);
			startingPkt = int(replytmp[(replytmp.index("X") + 1)])

		currentToken = tokens[0]; 
		msgNum = startingPkt + currentToken;
		if currentToken == tokens[0] : 
			tokens[0] = tokens[0] + totalTokens;
			#else tokens[1] = tokens[1] + totalTokens; 

     
    except socket.error, msg:
        print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()
