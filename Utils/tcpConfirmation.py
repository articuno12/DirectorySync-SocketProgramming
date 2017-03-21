# Function to send confirmation signal
def Send(conn) :
    # Send 1 for confirmation
    data = struct.pack('!I', 1) # Convert the numebr into string of size 4

    #keep sending the data till u have send all the data
    conn.sendall(data)

    return True

# Function to recieve confirmation signal , if no signal is returned within 1
# second it assumes not confirmed
def Receive(conn) :
    conn.setblocking(0)
    data = ''
    toberecieved = 4
    while toberecieved > 0 :
        ready = select.select([conn],[],[],1)
        if ready[0] :
            recieved = conn.recv(toberecieved)
            data = data + recieved
            toberecieved -= len(recieved)
        elif toberecieved == 4 :
            return False
    data, = struct.unpack('!I', data)

    return bool(data)
