import os #to execute needed os commands
import hashlib # to find MD5HashSum

def FindHash(path) :

    MD5HashSum = hashlib.md5()

    try :
        # Try opening the file
        f = open(path, 'rb')

    except:
        # You can't open the file for some reason
        f.close()
        raise Exception('Unable to read a file , Cannot genrate MD5HashSum : ' + path)

    # Read file in chunks and update the hashsum
    data = f.read(4096)
    while(data) :
        MD5HashSum.update(hashlib.md5(data).hexdigest())
        data = f.read(4096)

    # Close the file
    f.close()

    return MD5HashSum.hexdigest()
