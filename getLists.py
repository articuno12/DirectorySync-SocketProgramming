import os #to execute needed os commands
import re  # for checking regular expression

# Get Name,size,timestamp and type of each file in the current directory
def GetLongList() :
    LongList = []
    for filename in os.listdir('.') :

        # find path to the file to be passed to os.stat
        filepath = './' + filename
        stat = os.stat(filepath)

        #fileinfo = [ name of the file , last modification time , size of file]
        fileinfo = [ filename , stat.st_mtime , stat.st_size ]

        LongList.append(fileinfo)

    return LongList
