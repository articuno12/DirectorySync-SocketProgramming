import getMd5Hash #to find the hash of directories and files

# Find the hashsum and timestamp of all the files in the current directory
# and in the directories indside the current directory recursively
def VerifyAll(path) :
    # if no path is passed , assume current directory
    if not path :
        path ='./'

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
