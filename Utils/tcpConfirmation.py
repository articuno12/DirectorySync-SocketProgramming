# Function to send confirmation signal
def Send(conn) :
    # Send 1 for confirmation
    data = struct.pack('!I', 1) # Convert the numebr into string of size 4

    #keep sending the data till u have send all the data
    conn.sendall(data)

    return True
