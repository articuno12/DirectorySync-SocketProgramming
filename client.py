import select
import socket
import sys
import os
import Utils.getLists as getLists
import Utils.getMd5Hash as Md5Hash
import Utils.getVerification as getVerification
import Utils.globalValues as globalValues
import Utils.tcpFile as tcpFile
import Utils.tcpWord as tcpWord
import Utils.udpFile as udpFile
import Utils.getMd5Hash as getMd5Hash

# Open log file
logfile = open('log_client.txt','w')

def Execute(Command) :
    try :

        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.connect((globalValues.host, globalValues.port))

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        tcpWord.Send(conn,Command)

        Command = Command.split(' ')

        if Command[0] == 'index' :

            result = tcpWord.Recieve(conn)
            filename = 0
            timestamp = 1
            size = 2

            for fileinfo in result :
                print fileinfo[filename] , fileinfo[timestamp] ,fileinfo[size]

        elif Command[0] == 'download' :
            if Command[1] == 'tcp' :
                # if the recieved arguments are None => requested file was a file
                # else it was a directory
                tobedownloaded = tcpWord.Recieve(conn)

                # if the request was a directory
                if tobedownloaded :
                    # find the directories that have no file in them
                    directories = []
                    for fileinfo in tobedownloaded :
                        if fileinfo[1] == 'directory' :
                            directories.append(fileinfo[0])

                    # make the required directories
                    for directory in directories :
                        if not os.path.exists(directory) :
                            os.makedirs(directory)

                    for fileinfo in tobedownloaded :
                        if fileinfo[1] == 'file' :
                            path = fileinfo[0]
                            path = path.split('/')[:-1]
                            path = '/'.join(path)

                            if not os.path.exists(path) :
                                os.makedirs(path)


                    # download each file in the filelist
                    # first close the current port

                    tcp.close()
                    sock.close()
                    print >> logfile , "TCP port closed"
                    print >> logfile , "UDP port closed"
                    print >> logfile , "Command Executed successfully , directory structure recieved"

                    for fileinfo in tobedownloaded :

                        filepath = fileinfo[0]
                        # remove './' from path
                        filepath = filepath.split('/')
                        filepath = filepath[1:]
                        filepath = '/'.join(filepath)

                        # Make the download command
                        newcommand = 'download tcp ' + filepath
                        Execute(newcommand)

            elif Command[1] == 'udp' :

                # if the recieved arguments are None => requested file was a file
                # else it was a directory
                tobedownloaded = tcpWord.Recieve(conn)

                # if the request was a directory
                if tobedownloaded :
                    # find the directories that have no file in them
                    directories = []
                    for fileinfo in tobedownloaded :
                        if fileinfo[1] == 'directory' :
                            directories.append(fileinfo[0])

                    # make the required directories
                    for directory in directories :
                        if not os.path.exists(directory) :
                            os.makedirs(directory)

                    for fileinfo in tobedownloaded :
                        if fileinfo[1] == 'file' :
                            path = fileinfo[0]
                            path = path.split('/')[:-1]
                            path = '/'.join(path)

                            if not os.path.exists(path) :
                                os.makedirs(path)


                    # download each file in the filelist
                    # first close the current port

                    tcp.close()
                    sock.close()
                    print >> logfile , "TCP port closed"
                    print >> logfile , "UDP port closed"
                    print >> logfile , "Command Executed successfully , directory structure recieved"

                    for fileinfo in tobedownloaded :

                        filepath = fileinfo[0]
                        # remove './' from path
                        filepath = filepath.split('/')
                        filepath = filepath[1:]
                        filepath = '/'.join(filepath)

                        # Make the download command
                        newcommand = 'download udp ' + filepath
                        Execute(newcommand)

            else :
                pass

        elif Command[0] == 'hash' :
            if Command[1] == 'verify' :
                result = tcpWord.Recieve(conn)

                filename = 0
                timestamp = 1
                path = 2
                hashvalue = 3

                if not os.path.exists(result[path]) :
                    print "Name-",result[filename] ,"Timestamp-",result[timestamp][1] ,"Hash-",result[hashvalue], "Not Present"

                elif getMd5Hash.FindHash(result[path]) != result[hashvalue] :
                    print "Name-",result[filename] ,"Timestamp-",result[timestamp][1] ,"Hash-",result[hashvalue],"Modified"

                else :
                    print "Name-",result[filename] ,"Timestamp-",result[timestamp][1] ,"Hash-",result[hashvalue],"No Change"

            elif Command[1] == 'checkall' :

                resultlist = tcpWord.Recieve(conn)

                filename = 0
                timestamp = 1
                path = 2
                hashvalue = 3

                for result in resultlist :
                    if not os.path.exists(result[path]) :
                        print "Name-",result[filename] ,"Timestamp-",result[timestamp][1] ,"Hash-",result[hashvalue], "Not Present"

                    elif getMd5Hash.FindHash(result[path]) != result[hashvalue] :
                        print "Name-",result[filename] ,"Timestamp-",result[timestamp][1] ,"Hash-",result[hashvalue],"Modified"

                    else :
                        print "Name-",result[filename] ,"Timestamp-",result[timestamp][1] ,"Hash-",result[hashvalue],"No Change"

        else :
            pass

        
while True :
    try  :
        Command =  raw_input("input : ")
        # Command = 'index longlist'
        print >> logfile , "User Command is ",Command
        ConnectToListner(Command)

    except KeyboardInterrupt :
        print >> logfile , "Client Shutting Down"
        sys.exit(0)

    except Exception as e :
        print >> logfile , e
        print >> logfile , "Client Shutting Down"
        sys.exit(0)

logfile.close()
print "Client Closed"
