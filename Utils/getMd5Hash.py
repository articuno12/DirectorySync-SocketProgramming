import os #to execute needed os commands
import hashlib # to find MD5HashSum

def FindHash(path) :
    # defining utility varaiables
    FileChunkSize = 4096 # the ammout of data to read in one go from the file

    # Check if the path is a valid path that leades to a file or directory
    if not os.path.exists(path) :
        raise Exception('The given path does not exist. Cannot calculate MD5 - Hash \n The path passed is : ' + path)

    # Check if the given path is a file
    if not os.path.isfile(path) :

        HashValue = hashlib.md5()

        try :
            # Try opening the file
            f = open(path, 'rb')

        except:
            # Unable to  open the file
            f.close()
            raise Exception('The requested file cannot be opened. Cannot calculate MD5 - Hash \n The path passed is : ' + path)

        # Read file in chunks and update the hashsum
        data = f.read(FileChunkSize)
        while(data) :
            HashValue.update(hashlib.md5(data).hexdigest())
            data = f.read(FileChunkSize)

        # Close the file
        f.close()

    # Check if the given path is a directory
    elif os.path.isdir(path) :

        HashValue = hashlib.md5()
        try:
            for path2root, dirs, files in os.walk(path):
                for filename in files:
                    filepath = os.path.join(path2root,filename)

                    try :
                        # Try opening the file
                        f = open(filepath, 'rb')

                    except:
                        # You can't open the file for some reason
                        f.close()
                        raise Exception('The requested file cannot be opened. Cannot calculate MD5 - Hash \n The path passed is : ' + path)

                    # Read file in chunks and update the hashsum
                    data = f.read(FileChunkSize)
                    while(data) :
                        HashValue.update(hashlib.md5(data).hexdigest())
                        data = f.read(FileChunkSize)

                    # Close the file
                    f.close()
        except:
            import traceback
            # Print the stack traceback
            traceback.print_exc()
            raise Exception('Error Caused while finding the hashvalue')
            
    else :
        raise Exception('Function Implemented only to find MD5-Hash for files or directory. \n The given path is neither a file or directory.\n')

    # Return the hashvalue
    return HashValue.hexdigest()
