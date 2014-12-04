import socket
import sys
import time
 
HOST = '10.10.7.2'   # Symbolic name meaning all available interfaces
PORT = 8890 # Arbitrary non-privileged port
 
# Datagram (udp) socket
try :
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print 'Socket created'
except socket.error, msg :
    print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
 
 
# Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
 
firstround = 1
transtime = 0
file = open("ScenarioA.txt", "w") #C_1_3_2_1 , C 1_4 _2_1
#now keep talking with the client
while 1:
    # receive data from client (data, addr)
    d = s.recvfrom(1024)
    data = d[0]
    #print(data)
    addr = d[1]
     
    if not data: 
        break
     
    reply = 'OK...' + data
    logdata = data.split()

    if firstround == 1 :
        startime = time.time()
        firstround = 0
        file.write(str(startime) + ' ' + logdata[0] + '\n')
    else :
        recevtime = time.time()
        transtime = recevtime - startime
        file.write(str(transtime) + ' ' + logdata[0] + '\n')
     
    s.sendto(reply , addr)
    #print 'Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + data.strip()
    #print 'Message[' + addr1[0] + ':' + str(addr1[1]) + '] - ' + data1.strip()
    #datatmp = data.split()
    if(int(logdata[0]) % 100) == 0 :
        print(logdata[0] + " " + logdata[1] + " " + str(transtime))

    if int(logdata[0]) > 30099:
        file.close()
        break
s.close()
