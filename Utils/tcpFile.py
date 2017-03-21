import os # to execute system commands
import pickle # for serialization
import tcpWord
import select
import globalValues
import getMd5Hash

# To Send Files
def Send(conn,path) :

    # Check if this something we can send
    if not os.path.isdir(path) ot os.path.isfile(path) :
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
        tcp.Send(conn,'file')

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

    # Send file now
    try :
        # Try opening the file
        f = open(path, 'rb')

    except :
        # You can't open the file for some reason
        f.close()
        raise Exception('Unable to open the file for sending , Cannot send file : ' + path)

    # Read file in chunks and sent them
    totaltobesent = size

    while totaltobesent > 0 :
        # Send at max 10MB in 1 go
        data = f.read(min(MaxMB,totaltobesent))
        conn.sendall(data)
        totaltobesent -= len(data)

    # Close the file
    f.close()

    return None



# To Recieve Files
def RecieveFile(conn) :

    # Recieve Confirmation  that requested files is a file or directory
    confirmation = tcpWord.Recieve(conn)

    # If the requested file is not supported
    if confirmation == 'unkown' :
        return 'unkown','unkown'

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

    totaltoberecieved = info[size]

    conn.setblocking(0)

    # Receive file in chunks and write them in the current directory
    while totaltoberecieved > 0 :
        # Recieve at max 10MB in 1 go
        toberecieved = min(MaxMB,totaltoberecieved)
        data = ''

        while toberecieved > 0 :
            ready = select.select([conn],[],[],1)
            if ready[0] :
                recieved = conn.recv(toberecieved)
                data = data + recieved
                toberecieved -= len(recieved)

        totaltoberecieved -= len(data)
        # write the data into the file
        f.write(data)

    # close the file secriptor
    f.close()

    # Update permissions of the file
    os.chmod(path,info[permissions])

    # Update the timestamp of the file
    os.utime(path,info[timestamp])

    return None,None
