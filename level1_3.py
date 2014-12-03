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
tokens = []
reply = ""
while(1) :
    msg = str(msgNum) + " 3 "
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
		#print 'Server reply : ' + reply
		
		if reply != reply2 :
			#print 'Server reply : ' + reply
			replytmp = reply.split()
			indexX = replytmp.index("X");
			totalTokens = int(replytmp[0]);
			tokens = [];
			for i in range(1, indexX):
				tokens.append(int(replytmp[i]));
			if len(tokens) == 0 :
				tokens.append(0);
			#tokens = int(replytmp[indexX - 1]);
			startingPkt = int(replytmp[indexX + 1])

		currentToken = min(tokens);
		msgNum = startingPkt + currentToken;
		#print 'Before increment tokens[0] = ' + str(tokens[0]);
		for i in range(0, len(tokens)) :
			if tokens[i] == currentToken : 
				tokens[i] = tokens[i] + totalTokens;
		#print 'After increment tokens[0] = ' + str(tokens[0]);
     
    except socket.error, msg:
        print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()
