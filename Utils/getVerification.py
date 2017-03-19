import getMd5Hash #to find the hash of directories and files

# Find the hashsum and timestamp of all the files in the current directory
# and in the directories indside the current directory recursively
def VerifyAll(path) :
    # if no path is passed , assume current directory
    if not path :
        path ='./'

    if not os.path.isdir(path) :
        raise Exception('Verify All is expects a path to a directory . For single file use VerifyOne() ')

    data = []
    try:
        for path2root, dirs, files in os.walk(path):
            for filename in files:
                filepath = os.path.join(path2root,filename)

                # find the files timestamp
                stat = os.stat(filepath)

                # fileinfo = [ name , timestamp , path , hashvalue ]
                fileinfo = [filename , (stat.st_atime,stat.st_mtime) , filepath ,
                            getMd5Hash.FindHash(filepath)]

                data.append(fileinfo)
    except:
        import traceback
        # Print the stack traceback
        traceback.print_exc()
        raise Exception('Error Caused while finding the hashvalue')

    return data


def VerifyOne(path) :

    # find the filename
    filename = path.split('/')
    filename = filename[-1]

    # Check if its neither a file or directory
    if not os.path.isfile(path) and not os.path.isdir(path) :
        raise Exception('VerifyOne supports only file or directory. Unsupprted structure')

    # find the files timestamp
    stat = os.stat(path)

    fileinfo = [ filename , (stat.st_atime,stat.st_mtime) , path ,
                    getMd5Hash.FindHash(path)]

    return entry
