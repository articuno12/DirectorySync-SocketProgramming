import os #to execute needed os commands
import re  # for checking regular expression

# Get Name,size,timestamp and type of each file in the current directory
def FindLongList() :
    LongList = []
    for filename in os.listdir('.') :

        # find path to the file to be passed to os.stat
        filepath = './' + filename
        stat = os.stat(filepath)

        #fileinfo = [ name of the file , last modification time , size of file]
        fileinfo = [ filename , stat.st_mtime , stat.st_size ]

        LongList.append(fileinfo)

    return LongList

# Get Name,size,timestamp and type of each file in the directory
# having timestamp between starttimestamp and endtimestamp
def FindShortList(StartTimeStamp,EndTimeStamp) :
    # Utility Varaiables
    Name = 0
    Mtime = 1
    Size = 2

    ShortList = []
    # first acquire info about all the files and then filter
    LongList = FindLongList()

    for fileinfo in Longlist :
        if fileinfo[Mtime] >= StartTimeStamp and fileinfo[Mtime] <= EndTimeStamp :
            ShortList.append(fileinfo)

    return ShortList
