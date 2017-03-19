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

        return HashValue.hexdigest()
