import pickle # for serialization
import struct # to store numbers into string of fixed length
import globalValues
import select

# To send data of at max size 10 MB
def SendWord(conn,data) :
    # Searile the data
    data = pickle.dumps(data)

    # assert that data to be sent after searialization is at max 10MB
    if not len(data) <= globalValues.MaxSize :
        raise Exception('Chunk with size > max allowed size ')

    # First send the length of incoming data to the client
    length = struct.pack('!I', len(data)) # Convert the numebr into string of size 4

    #keep sending the data till u have send all the data
    conn.sendall(length)

    # Now send the actual data
    conn.sendall(data)
    return True


# To recieve data of at max fize 10 MB
def RecieveWord(conn) :
    # First recieve the total length of the incoming data
    conn.setblocking(0)
    data = ''
    toberecieved = 4
    while toberecieved > 0 :
        ready = select.select([conn],[],[],1)
        if ready[0] :
            recieved = conn.recv(toberecieved)
            data = data + recieved
            toberecieved -= len(recieved)
    data, = struct.unpack('!I', data)

    toberecieved = data
