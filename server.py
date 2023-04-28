import socket
import hashlib
import time

class mitigationServer:
	tic = time.perf_counter() 
	localIP     = "127.0.0.1"
	localPort   = 20001
	bufferSize  = 1024
	#k=0
	#constant=200
	
	def check_hash(self,hash1):
		noz=0
		k=0
		while(k<len(hash1)):
			if(hash1[k]==0):
				noz=noz+1
				k=k+1
			else :
				return noz
		return noz
	
	
	def isWorkDone(self,constant,nonce,diff):
		hash_read=[100]
		noz=0
		total=0
		tot=''
		str=[1000]
		non=int(nonce)
		total=constant+non
		tot= "%s" %total
		hashed_string = hashlib.sha256(tot.encode('utf-8')).hexdigest()
		print("Hash: ",hashed_string)
		noz=self.check_hash(hashed_string)
		if(noz==diff):
			return 1
		else:
			return 0
		return noz
	
	def startServer(self):
		#start_networking();
		tic = time.perf_counter() 
		localIP     = "127.0.0.1"
		localPort   = 20001
		bufferSize  = 1024
		solved=0
		UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
		# Bind to address and ip
		UDPServerSocket.bind((localIP, localPort))
		print("UDP server up and listening")
		bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
		message = bytesAddressPair[0]
		address = bytesAddressPair[1]
		#address = {"10.0.0.8",6633}
		#print(address)
		clientMsg = "Message from Client:{}".format(message)
		clientIP  = "Client IP Address:{}".format(address)
		#print(clientMsg)
		#print(clientIP)
		dif=1
		#address="10.0.0.8"
		bytesToSend= str.encode(str(dif))
		UDPServerSocket.sendto(bytesToSend, address)
		#tic = time.perf_counter()
		diff=int(dif)
		while(diff<5):
			print("Difficulty: ",diff)
			bytesToSend= str.encode(str(diff))
			UDPServerSocket.sendto(bytesToSend, address)
			bytesAddressPair=UDPServerSocket.recvfrom(bufferSize)
			con= bytesAddressPair[0]
			constant=int(con)
			bytesAddressPair=UDPServerSocket.recvfrom(bufferSize)
			non = bytesAddressPair[0]
			nonce=int(non)
			print("Constant: ",constant)
			print("Nonce: ",nonce)
			if(self.isWorkDone(constant,nonce,diff)==0):
				print("Puzzle solved for difficulty: ",diff)
				print("\n")
				solved=solved+1
			else:
				print("Puzzle not solved for difficulty: ",diff)
				print("Access to server denied\n")
				print("\n")
				exit(-1)
			diff=diff+1;
			p=diff;

		toc = time.perf_counter()
		if(solved==p-1):
			print("Solved for all difficuilties")
			print("Checking for time taken to solve.......")
		    
		else:
			print("Access Denied.....:)\n")
			exit(-1)
		    
		print(f"Time taken to complete puzzle is : {toc - tic:0.4f} seconds")    
		if(toc - tic<15):
			print("Access Granted.....:D\n")
			#exit(0)
		   
		else:
			print("Time exceeded....")
			print("Better luck next time......")
			print("Access Denied.....:(\n")
			exit(-1)
				
	def start_networking():
        #while(True):
        # Create a datagram socket
		UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        # Bind to address and ip
		UDPServerSocket.bind((localIP, localPort))
		print("UDP server up and listening")
  	
	
		        		
def __init__(self):
    pass
