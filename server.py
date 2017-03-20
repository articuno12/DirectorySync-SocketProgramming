import select
import socket
import Utils.getLists as getLists
import Utils.getMd5Hash as Md5Hash
import Utils.getVerification as getVerification
import Utils.globalValues as globalValues


# SET UP TCP
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# to force the OS to free the port
# if the port was in use earlier it will be taken and assigned to the current program
# use with care
tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

tcp.bind((globalValues.host, globalValues.port))
tcp.listen(2)

# SET UP UDP
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind((globalValues.host,globalValues.port))

logfile = open('log_server.txt','w')

while True:
    conn, addr = s.accept()
    print 'Got connection from', addr
    data = conn.recv(1024)
    print "Second Timed data is" , data

    print('Server received', repr(data))

    f = open(filename,'rb')
    l = f.read(1024)
    while (l):
       conn.send(l)
       print('Sent ',repr(l))
       l = f.read(1024)
    f.close()

    print('Done sending')
    conn.send('Thank you for connecting')
    conn.close()
