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
tokens = []
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
		#print 'Server reply : ' + reply
		#print 'Server reply : ' + reply + ' INDEX: ' + str(indexB)
		#print 'Server replytmp : ' + replytmp[indexB + 1] + " " + replytmp[indexB + 2]
	
		if reply != reply2 :
			replytmp = reply.split()
			indexB = replytmp.index("B")
			indexY = replytmp.index("Y")
			totalTokens = int(replytmp[indexB + 1]);
			tokens = [];
			for i in range(indexB + 2, indexY):
				tokens.append(int(replytmp[i]));
			if len(tokens) == 0 :
				tokens.append(0);
			#tokens = int(replytmp[indexX - 1]);
			startingPkt = int(replytmp[indexY + 1])

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
