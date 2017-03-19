import Utils.getLists as getLists
import Utils.getMd5Hash as Md5Hash
import Utils.getVerification as getVerification

port = 60000
host = ""

port = 60000
s = socket.socket()
host = ""

# to force the OS to free the port
# if the port was in use earlier it will be taken and assigned to the current program
# use with care
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
s.listen(5)

filename = raw_input("Enter file to share:")
print 'Server listening....'

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
