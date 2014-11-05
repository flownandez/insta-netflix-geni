import socket
import sys
 
HOSTrecv1 = '10.10.5.2'   # Symbolic name meaning all available interfaces
PORTrecv1 = 8889 # Arbitrary non-privileged port
HOSTrecv2 = '10.10.6.2'   # Symbolic name meaning all available interfaces
PORTrecv2 = 8888 # Arbitrary non-privileged port
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
# try :
#     srecev2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     print 'Socket created'
# except socket.error, msg :
#     print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
#     sys.exit()
# # Bind socket to local host and port
# try:
#     srecev2.bind((HOSTrecv2, PORTrecv2))
# except socket.error , msg:
#     print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
#     sys.exit()
# print 'Socket bind complete'

# ############### Datagram (udp) SEND socket ###############
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
 
############### now keep talking with the client ###############
while 1:
    # receive data from client (data, addr)
    d1 = srecev1.recvfrom(1024)
    data1 = d1[0]
    addr1 = d1[1]
     
    if not data1: 
        break
     
    reply1 = 'OK...' + data1
     
    srecev1.sendto(reply1 , addr1)
    print 'Message[' + addr1[0] + ':' + str(addr1[1]) + '] - ' + data1.strip()

    # # receive data from client (data, addr)
    # d2 = srecev2.recvfrom(1024)
    # data2 = d2[0]
    # addr2 = d2[1]
     
    # if not data2: 
    #     break
     
    # reply2 = 'OK...' + data2
     
    # srecev2.sendto(reply2 , addr2)
    # print 'Message[' + addr2[0] + ':' + str(addr2[1]) + '] - ' + data2.strip()

    # send data from clients (data, addr) to layer 3
    newdata = d1[0] #+ ' ' + d2[0] 
    newaddr = (HOSTsend, PORTsend)
          
    ssend.sendto(newdata , newaddr)     
#s.close(
