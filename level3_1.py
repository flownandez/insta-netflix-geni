import socket
import sys
import time
import select

HOSTrecv1 = '10.10.5.2'   # Symbolic name meaning all available interfaces
PORTrecv1 = 8889 # Arbitrary non-privileged port
HOSTrecv2 = '10.10.6.2'   # Symbolic name meaning all available interfaces
PORTrecv2 = 9001 # Arbitrary non-privileged port
HOSTsend = '10.10.7.2'
PORTsend = 8890
 
############### Datagram (udp) RECEV1 socket ###############
try :
    srecev1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print 'Socket created'
except socket.error, msg :
    print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
# Bind socket to local host and port
try:
    srecev1.bind((HOSTrecv1, PORTrecv1))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
print 'Socket bind complete'

############### Datagram (udp) RECEV2 socket ###############
try :
    srecev2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print 'Socket created'
except socket.error, msg :
    print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
# Bind socket to local host and port
try:
    srecev2.bind((HOSTrecv2, PORTrecv2))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
print 'Socket bind complete'

############### Datagram (udp) SEND socket ###############
# try :
#     ssend = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     print 'Socket created'
# except socket.error, msg :
#     print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
#     sys.exit()
# # Bind socket to local host and port
# try:
#     ssend.bind((HOSTsend, PORTsend))
# except socket.error , msg:
#     print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
#     sys.exit()
# print 'Socket bind complete'
 
try:
    ssend = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()

startTime = time.time();
prevTime = time.time();
oneSecond = 0;
reply2_1 = "2 0 X 1 B 2 1 Y 1"
reply2_2 = "2 0 X 1 B 2 1 Y 1"
pps1 = 0
pps2 = 0 
pps3 = 0
pps4 = 0
newDataPkt = 0
seconds = 0;
packetsReceived = [];
previousMessages = [" ", " ", " ", " "];
for i in range(30101) :
	packetsReceived.append(0) ;

############### now keep talking with the client ###############
while 1:
	newTime = time.time();
	if((newTime - prevTime) >= 1) : 
		prevTime = time.time();
		oneSecond = 1;
		seconds = seconds + 1; 					
		#this part finds the lowest packets per second of any level1 node
		lowest = min(pps1, pps2, pps3, pps4);
		
		#print "pps1: ------  " + str(pps1)		
		#print "pps2: ------  " + str(pps2)
		#print "pps3: ------  " + str(pps3)
		#print "pps4: ------  " + str(pps4)		

		
		#this is where the number of tokens each level1 node gets are assigned
		if(lowest == 0) :	#this will happen on startup or when we are testing only a couple of the nodes
			if(pps1 == 0): 
				tokensToAllocate1 = 0;
			else:
				tokensToAllocate1 = 1;
			if(pps2 == 0): 
				tokensToAllocate2 = 0;
			else:
				tokensToAllocate2 = 1;
			if(pps3 == 0): 
				tokensToAllocate3 = 0;
			else:
				tokensToAllocate3 = 1;
			if(pps4 == 0): 
				tokensToAllocate4 = 0;
			else:
				tokensToAllocate4 = 1;
			
		else :		
			if(pps1 == 0): 
				tokensToAllocate1 = 0; 		
			elif(pps1 < (lowest + 5)) :
				tokensToAllocate1 = 1;	 #if pps1 is close to lowest, give it 1 token
			else : 			
				tokensToAllocate1 = int(pps1 / lowest);  #else give it tokens proportional to its pps compared to lowest
				                                   				# can hardcode to 2 if issues

			if(pps2 == 0) :
				tokensToAllocate2 = 0;	
			elif(pps2 < (lowest + 5)):
				tokensToAllocate2 = 1; #do the same for all nodes
			else :
				tokensToAllocate2 = int(pps2 / lowest); 

			if(pps3 == 0):
				tokensToAllocate3 = 0; 	
			elif(pps3 < (lowest + 5)):
				tokensToAllocate3 = 1;
			else:
				tokensToAllocate3 = int(pps3 / lowest);

			if(pps4 == 0):
				tokensToAllocate4 = 0; 	
			elif(pps4 < (lowest + 5)):
				tokensToAllocate4 = 1;
			else:
				tokensToAllocate4 = int(pps4 / lowest);

		totalTokens = tokensToAllocate1 + tokensToAllocate2 + tokensToAllocate3 + tokensToAllocate4;
		if (totalTokens == 0) :
			tokensToAllocate1 = 1;
			tokensToAllocate2 = 1;
			tokensToAllocate3 = 1;
			tokensToAllocate4 = 1;
			totalTokens = 4; 

		#this is where we assign the tokens to each node
		tokenNumber = 0; #first token to assign will be 0
		message1 = "" + str(totalTokens); #first part of messages will be total number of tokens
		message2 = "" + str(totalTokens);
		message3 = "" + str(totalTokens);
		message4 = "" + str(totalTokens);

		#these variables will keep track of how many tokens each node has been assigned
		tokensAllocated1 = 0
		tokensAllocated2 = 0
		tokensAllocated3 = 0
		tokensAllocated4 = 0

		while tokenNumber < totalTokens : #perform until all tokens are allocated
			#print "tokenNumber: " + str(tokenNumber) + " --- totalTokens: " + str(totalTokens)
			#print "tokensAllocated1: " + str(tokensAllocated1) + " --- tokensToAllocate1: " + str(tokensToAllocate1)					
			if(tokensAllocated1 < tokensToAllocate1):
				if (tokenNumber < totalTokens) :
					#print "MESSAGE 1 : " + message1
					message1 = message1 + " " + str(tokenNumber); #allocate token by adding token number to message
					tokenNumber = tokenNumber + 1; #increment token number
					tokensAllocated1 = tokensAllocated1 + 1; #node 1 has been assigned 1 more token

			if(tokensAllocated2 < tokensToAllocate2):
				if(tokenNumber < totalTokens) :
					message2 = message2 + " " + str(tokenNumber);
					tokenNumber = tokenNumber + 1; #increment token number
					tokensAllocated2 = tokensAllocated2 + 1;

			if(tokensAllocated3 < tokensToAllocate3):
				if(tokenNumber < totalTokens) :
					message3 = message3 + " " + str(tokenNumber);
					tokenNumber = tokenNumber + 1; #increment token number
					tokensAllocated3 = tokensAllocated3 + 1;

			if(tokensAllocated4 < tokensToAllocate4) :
				if(tokenNumber < totalTokens) :
					message4 = message4 + " " + str(tokenNumber);
					tokenNumber = tokenNumber + 1; #increment token number
					tokensAllocated4 = tokensAllocated4 + 1;
				
		startingPkt = packetsReceived.index(0); 
		
		if (tokensAllocated1 == 0):
			message1 = message1 + " 0";
		if (tokensAllocated2 == 0):
			message2 = message2 + " 0";
		if (tokensAllocated3 == 0):
			message3 = message3 + " 0";
		if (tokensAllocated4 == 0):
			message4 = message4 + " 0";
		
		if previousMessages == [message1, message2, message3, message4] :
			previousMessages = [message1, message2, message3, message4];
			if(seconds == 10) :
				seconds = 0;
				previousMessages = [message1, message2, message3, message4];
				message1 = message1 + " X " + str(startingPkt); #message format will be "totalTokens tokens[..] X startingPkt"
				message2 = message2 + " Y " + str(startingPkt);
				message3 = message3 + " X " + str(startingPkt);
				message4 = message4 + " Y " + str(startingPkt);
				reply2_1 = message1 + " B " + message2;
				reply2_2 = message3 + " B " + message4;
			 
		else :
			#print 'New Message'
			previousMessages = [message1, message2, message3, message4];
			message1 = message1 + " X " + str(startingPkt); #message format will be "totalTokens tokens[..] X startingPkt"
			message2 = message2 + " Y " + str(startingPkt);
			message3 = message3 + " X " + str(startingPkt);
			message4 = message4 + " Y " + str(startingPkt);
			reply2_1 = message1 + " B " + message2;
			reply2_2 = message3 + " B " + message4;

		pps1 = 0 #reset counters
		pps2 = 0 
		pps3 = 0
		pps4 = 0

	readySockets, blank1, blank2 = select.select([srecev1, srecev2], [], []);
	for sock in readySockets:
		d = sock.recvfrom(1024);
		data = d[0]
    		addr = d[1]
		if not data: 
        		break

		if(addr[0] == '10.10.5.1') :
			reply = reply2_1;
		else :
			reply = reply2_2; 
		
		sock.sendto(reply , addr) 
		
		#print 'Message[' + addr1[0] + ':' + str(addr1[1]) + '] - ' + data1.strip()
		datatmp = data.split()
		newDataPkt = int(datatmp[0])
		#print(datatmp[0] + " " + datatmp[1])
		if(int(datatmp[1]) == 1) :
			pps1 = pps1 + 1;
		if(int(datatmp[1]) == 2) :
			pps2 = pps2 + 1;
		if(int(datatmp[1]) == 3) :
			pps3 = pps3 + 1;
		if(int(datatmp[1]) == 4) :
			pps4 = pps4 + 1;
		
		packetsReceived[int(datatmp[0])] = 1; 	
		if(int(datatmp[0]) > 30100) : 	#stop after 30000 packets
			srecev1.close();
			srecev2.close();
			break;
		# send data from clients (data, addr) to layer 4
		newdata = d[0] 
		print newdata
		newaddr = (HOSTsend, PORTsend)
		ssend.sendto(newdata , newaddr) 

#s.close()
