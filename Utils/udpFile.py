import os # to execute system commands
import pickle # for serialization
import tcpWord
import tcpConfirmation
import select
import globalValues
import getMd5Hash
import struct

# To Send Files via Udp
# sock : the udp socket
# conn : the tcp socket
def Send(conn,sock,path) :

    # Check if this something we can send
    if not (os.path.isdir(path) or os.path.isfile(path)) :
        # something this program in developed to handle
        # tell client that this file cannot be transfered
        tcpWord.Send(conn,'unkown')
        return None

    # Check if the asked is a directory
    if os.path.isdir(path) :
        # Notify the client that file requested is a directory
        tcpWord.Send(conn,'directory')

        # Get the list of file paths and directory paths
        tobedownloaded = []

        try:
            for path2root, dirs, files in os.walk(path):

                # Check for those directories that have no file in them
                if len(dirs) == 0 and len(files) == 0 :
                    entry = [path2root ,'directory']
                    tobedownloaded.append(entry)

                for filename in files:

                    filepath = os.path.join(path2root,filename)
                    entry = [ filepath ,  'file']
                    tobedownloaded.append(entry)
        except:
            import traceback
            # Print the stack traceback
            traceback.print_exc()
            raise Exception('Error Caused while Finding which files need to be sent')

        # Send the file structure to the client
        tcpWord.Send(conn,tobedownloaded)

        return None

    else :
        tcpWord.Send(conn,'file')

    # Store the details about the file
    hashvalue = getMd5Hash.FindHash(path)
    # Find details about the file
    stat = os.stat(path)

    permissions = stat.st_mode
    timestamp = (stat.st_atime,stat.st_mtime) #(last access,last modified)
    size = stat.st_size # size of file in bytes

    # Find the name of the file
    filename = path
    filename = filename.split('/')
    filename = filename[-1]

    # info = [name , timestamp, path, hash,size ,permissions]
    info = [filename,timestamp,path,hashvalue,size,permissions]

    # Send the details to the client
    tcpWord.Send(conn,info)

    # Look for HandShake
    toberecieved = len('HandShake')
    recieved,address = sock.recvfrom(toberecieved)

    # HandShake Complete , signal the other side of the confirmation
    tcpConfirmation.Send(conn)

    # Send file now
    try :
        # Try opening the file
        f = open(path, 'rb')

    except:
        # You can't open the file for some reason
        f.close()
        raise Exception('Unable to read a file , Cannot send file : ' + path)

    # total number of bytes to be send
    totaltobesent = size

    # Count of the number of packets already sent
    packetIndex = 0

    while totaltobesent > 0 :
        # Send at max globalValues.MaxSize  in 1 go
        data = f.read(min(globalValues.MaxSize,totaltobesent))

        # To avoid duplicay of the packets add to the data the packet number
        # Convert the packet into a fixed length = 4 bytes string and append to
        # the data
        IndexString = struct.pack('!I', packetIndex)
        newdata = data + IndexString

        success = False

        while not success :
            # Send the data using udp port
            sock.sendto(newdata,address)

            # wait for confirmation via TCP
            success = tcpConfirmation.Receive(conn)

        # Confirm the packet has been recieved
        totaltobesent -= len(data)
        packetIndex += 1

    # Close the file
    f.close()

    return None


# To Recieve Files via UDP
# sock : the udp socket
# conn : the tcp socket
def Recieve(conn,sock) :

    # Recieve Confirmation  that requested files is a file or directory
    confirmation = tcpWord.Recieve(conn)

    # If the requested file is not supported
    if confirmation == 'unkown' :
        return 'unkown'

    # If the Requested file is a directory
    elif confirmation == 'directory' :

        # Recieve directory and file structure
        tobedownloaded = tcpWord.Recieve(conn)

        return tobedownloaded

    info = tcpWord.Recieve(conn)

    #Utility Varaiables
    name = 0
    timestamp = 1
    path = 2
    hashindex = 3
    size = 4
    permissions = 5

    path = info[path]

    try :
        # opening the file to write
        f = open(path,'wb')

    except:
        # You can't open the file for some reason
        f.close()
        raise Exception('Unable to Open the file for writing , Cannot recieve file : ' + path)


    # Perform Handshake
    HandshakeSuccessful = False
    while not HandshakeSuccessful :
        sock.sendto('HandShake',(globalValues.host,globalValues.port))
        HandshakeSuccessful = tcpConfirmation.Receive(conn)


    totaltoberecieved = info[size]

    # The package number that should be arriving now
    expectedPackageIndex = 0

    # Receive file in chunks and write them in the current directory
    while totaltoberecieved > 0 :
        # Recieve at max 10MB in 1 go
        # +4 for the package Index attached to the original data
        toberecieved = min(globalValues.MaxSize,totaltoberecieved) + 4

        # Recieve data via udp
        recieved,address = sock.recvfrom(toberecieved)

        # current recieved contains the actual data and last 4 bytes as the package
        # number . We need to seprate them .
        recievedPackageIndex = recieved[-4:]
        recievedPackageIndex, = struct.unpack('!I', recievedPackageIndex)

        # Check for duplicate package
        if not recievedPackageIndex == expectedPackageIndex :
            print "Recieved package index ",recievedPackageIndex
            print "Expected Package index ",expectedPackageIndex
            continue

        data = recieved[:-4]

        # Send confirmation to the other side
        tcpConfirmation.Send(conn)

        totaltoberecieved -= len(data)
        expectedPackageIndex += 1

        # write the data into the file
        f.write(data)

    # close the file secriptor
    f.close()

    # Update permissions of the file
    os.chmod(path,info[permissions])

    # Update the timestamp of the file
    os.utime(path,info[timestamp])

    return None
