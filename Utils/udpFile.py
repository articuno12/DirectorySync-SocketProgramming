import os # to execute system commands
import pickle # for serialization
import tcpWord
import tcpConfirmation
import select
import globalValues
import getMd5Hash

# To Send Files via Udp
# sock : the udp socket
def Send(conn,sock,path) :

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
        tcpWord.send(conn,'file')

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

    