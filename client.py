import socket
import hashlib
import time
 
serverAddressPort = ("127.0.0.1", 20001)
bufferSize = 1024

def check_hash(hash1):
    noz=0
    k=0
    while(k<len(hash1)):
        if(hash1[k]=='0'):
            noz=noz+1
            k=k+1
        else:
            return noz
    return noz  
         

def get_nonce(constant,diff):
    hash_read=''
    noz=0
    nonce=0
    total=0
    str=''
    temp_string=''
    print(diff)
    while(noz!=int(diff)):
        total=constant+nonce
        tot="%s" %total
        hashed_string = hashlib.sha256(tot.encode('utf-8')).hexdigest()
        print("Hash: ",hashed_string)
        noz=check_hash(hashed_string)
        print("Total: ",total)
        print("Constant: ",constant)
        print("Nonce: ",nonce)
        print("Noz: ",noz)
        print("\n")
        nonce=nonce+1
    return nonce-1


def main():
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    msgFromClient = "Hello UDP Server"
    bytesToSend = str.encode(msgFromClient)
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    msg = "Message from Server {}".format(msgFromServer[0])
    print(msg)
    diff=0
    nonce=0
    constant=200
    temp_string=''
    while(True):
        msgFromServer = UDPClientSocket.recvfrom(bufferSize)
        msg="Difficulty is: {}".format(msgFromServer[0])
        dif=msgFromServer[0]
        print(dif)
        diff=int(dif)
        nonce=get_nonce(constant,diff)
        print("Constant: ",constant)
        print(" Nonce: ",nonce)
        msgFromClient=str(constant)
        bytesToSend= str.encode(msgFromClient)
        UDPClientSocket.sendto(bytesToSend, serverAddressPort)
        msgFromClient=str(nonce)
        bytesToSend= str.encode(msgFromClient)
        UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    return 0
    
if __name__ == "__main__":
    main()
