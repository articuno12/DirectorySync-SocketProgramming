import select
import socket
import Utils.getLists as getLists
import Utils.getMd5Hash as Md5Hash
import Utils.getVerification as getVerification
import Utils.globalValues as globalValues
import Utils.tcpFile as tcpFile
import Utils.tcpWord as tcpWord
import Utils.udpFile as udpFile

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
    try :
        print >> logfile , "Server Listening ..."
        conn, addr = tcp.accept()
        print >> logfile , 'Got connection from ip :', addr[0] , ' port : ',addr[1]

        # Listen to the request from the client
        request = tcpWord.Recieve(conn)

        print >> logfile , 'Server recieved request : ',request

        request = request.split(' ')

        if request[0] == 'index' :
            if request[1] == 'longlist' :
                ans = getLists.FindLongList()

            elif request[1] == 'shortlist' :
                ans = getLists.FindShortList(int(request[2]),int(request[3]))

            elif request[1] == 'regex':
                ans = getLists.GetRegList(request[2])

            tcpWord.Send(conn,ans)

        elif command == 'download' :

            if request[1] == 'tcp' :
                tcpFile.Send(conn,'./' + request[2])

            elif request[1] == 'udp' :
                udpFile.Send(conn,udp,'./' + request[2])

            else :
                # Invalid flag
                pass

        elif command == 'hash' :
            if request[1] == 'verify' :
                ans = getVerification.VerifyOne('./' + request[2])
                tcpWord.Send(conn,ans)

            elif request[1] == 'checkall' :
                ans = getVerification.VerifyAll()

            else :
                pass
        else :
            pass

        # close the Connection
        conn.close()

    
