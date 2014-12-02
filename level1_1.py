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
tokens = []
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
		print 'Server reply : ' + reply
		
		if reply != reply2 :
			replytmp = reply.split()
			indexX = replytmp.index("X");
			totalTokens = int(replytmp[0]);
			tokens = [];
			for i in range(1, indexX):
				tokens.append(int(replytmp[i]));
			#tokens = int(replytmp[indexX - 1]);
			startingPkt = int(replytmp[indexX + 1])

		currentToken = min(tokens);
		msgNum = startingPkt + currentToken;
		print 'Before increment tokens[0] = ' + tokens[0];
		for token in tokens :
			if currentToken == token : 
				token = token + totalTokens;
				#else tokens[1] = tokens[1] + totalTokens; 
		print 'After increment tokens[0] = ' + tokens[0];
     
    except socket.error, msg:
        print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()
