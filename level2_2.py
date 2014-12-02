import socket
import sys
import select

HOSTrecv1 = '10.10.3.2'   # Symbolic name meaning all available interfaces
PORTrecv1 = 8887 # Arbitrary non-privileged port
HOSTrecv2 = '10.10.4.2'   # Symbolic name meaning all available interfaces
PORTrecv2 = 8888 # Arbitrary non-privileged port
HOSTsend = '10.10.6.2'
PORTsend = 9001
 
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

reply = "2 0 X 1 B 2 1 Y 1"  
############### now keep talking with the client ###############
while 1:
   	readySockets, blank1, blank2 = select.select([srecev1, srecev2, ssend], [], []);
	for sock in readySockets:
		d = sock.recvfrom(1024);
		data = d[0]
    		addr = d[1]
		if not data: 
        		break
		
		if(addr[0] == HOSTsend) :
			reply = data; 	 	

		else :	 
			#print addr[0]
			sock.sendto(reply , addr)
			#print 'Message[' + addr1[0] + ':' + str(addr1[1]) + '] - ' + data1.strip()
			datatmp = data.split()
			#print(datatmp[0] + " " + datatmp[1])

			# send data from clients (data, addr) to layer 4
			newdata = d[0] 
			newaddr = (HOSTsend, PORTsend)
			ssend.sendto(newdata , newaddr) 
#s.close()
