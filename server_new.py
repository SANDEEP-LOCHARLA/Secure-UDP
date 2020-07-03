import socket
import threading
import hashlib
import time
import datetime



delimiter = "|:|:|";

# Packet class definition
class packet():
    seqFlag = 0;
    checksum = 0;
    length = 0;
    seqNo = 0;
    msg = 0;

    def make(self, data):
        self.checksum=hashlib.sha1(data).hexdigest()
        self.msg = data
        self.length = str(len(data))
        print(("Length: "+str(self.length)+"\nSequence number: "+str(self.seqNo))) 


# Connection handler
def handleConnection(address, data):
    packet_count=0
    time.sleep(0.5)
    start=time.time()
    pkt = packet()
    print(("Request started at: " + str(datetime.datetime.utcnow())))
    threadSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Read requested file

        try:
            print(("The requested file is "+data))
            print("Opening the file... ")
            fileRead = open(data, 'r')
            data = fileRead.read()
            print("file closed...")
            fileRead.close()
        except:
            print("the requested file is not present...")
            msg="FNF";
            pkt.make(msg);
            print("replied with FNF...")
            finalPacket = str(pkt.checksum) + delimiter + str(pkt.seqNo) + delimiter + str(pkt.length) + delimiter + pkt.msg
            print('sending...')
            threadSock.sendto(finalPacket, address)
            return

        # Fragment and send file 500 byte by 500 byte
        totpkts = len(data) / 500
	bits = len(data)
	tim = 0
        x = 0
	stt = time.time()
        while x < totpkts + 1:
            msg = data[x * 500:x * 500 + 500];
            pkt.make(msg);
            packet_count = packet_count + 1
            finalPacket = str(pkt.checksum) + delimiter + str(pkt.seqNo) + delimiter + str(pkt.length) + delimiter + pkt.msg
            # Send packet
            print('sending...')
            sent = threadSock.sendto(finalPacket, address)
            print(('Sent '+str(sent)+' bytes back to '+str(address)+' with seq no: '+str(pkt.seqNo)))
            print('awaiting acknowledgment..')
            threadSock.settimeout(2)
            try:
                ack, address = threadSock.recvfrom(100);
            except:
                print(("Time out reached, resending ..."+x))
                continue;
            if ack.split(",")[0] == str(pkt.seqNo):
                tim = tim + (time.time() - stt)
                pkt.seqNo = int(not pkt.seqNo)
                print(("Acknowledged by: " +str(ack) + "\nAcknowledged at: " + str(datetime.datetime.utcnow()) + "\nElapsed: " + str(time.time() - stt)))
		stt = time.time()
                x = x + 1
        print(("Packets served: " + str(packet_count)))
	print("Throughput: " + str(bits/tim)+" bps")
	print(tim)
    except:
        print("Internal server error")

ip = input('enter the ip address as a string: ')
port1 = input('enter the port number: ')
server_address = (ip, port1)
# Start - Connection initiation
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(server_address)

# Listening for requests indefinitely
while True:
    print ('Waiting to receive message')
    data, address = sock.recvfrom(600)
    print('received data..')
    print(('Received '+str(len(data))+' bytes from '+str(address)))
    print(data)
    connectionThread = threading.Thread(target=handleConnection, args=(address, data))
    connectionThread.start()
    

