import select
import socket
import sys
import Utils.getLists as getLists
import Utils.getMd5Hash as Md5Hash
import Utils.getVerification as getVerification
import Utils.globalValues as globalValues
import Utils.tcpFile as tcpFile
import Utils.tcpWord as tcpWord
import Utils.udpFile as udpFile

# Open log file
logfile = open('log_client.txt','w')



while True :
    try  :
        Command =  raw_input("input : ")
        # UserCommand = 'index longlist'
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
