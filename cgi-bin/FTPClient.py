#FTPClient.py

from socket import socket, AF_INET, SOCK_STREAM
from ast import literal_eval
import time

def send(socket, msg): 
	print "===>sending: " + msg
	socket.send(msg + "\r\n")
	recv = socket.recv(2048)
	print "<===receive: " + recv
	return recv
	
def builtport(message):
	start = message.find("(")
	end  = message.find(")")
	tuple = message[start+1:end].split(',')
	print tuple
	#build the port from the last two numbers
	port = int(tuple[4])*256 + int(tuple[5])
	print port
	return port
	
serverName = 'ftp.swfwmd.state.fl.us'
serverPort = 21
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
condition = True
message = clientSocket.recv(2048)
print message
while condition:
	message = clientSocket.recv(2048)
	print message
	condition = message[0:6] != "220---"
message = send(clientSocket,"USER Anonymous")
message = send(clientSocket,"PASS abc@fiu.edu")
message = send(clientSocket,"TYPE A")
message = send(clientSocket,"PASV")
start = message.find("(")
end  = message.find(")")
tuple = message[start+1:end].split(',')
print tuple
#build the port from the last two numbers
port = int(tuple[4])*256 + int(tuple[5])
print port
dataSocket = socket(AF_INET, SOCK_STREAM)
dataSocket.connect((serverName, port))

#Download a FILE
message = send(clientSocket,"RETR README.txt")
start = message.find("(")
end  = message.find(")")
byteNum = message[start+1:end].split()[0]
print byteNum

#Loop until all bytes are recieved.
while byteNum > 0:
	message = dataSocket.recv(2048)
	print message
	byteNum = int(byteNum) - len(message)

message = clientSocket.recv(2048)
print message

#CHANGE DIRECTORY
message = send(clientSocket,"CWD public")
#LIST ITEMS OVER A NEW TCP DATA CONNECTION
message = send(clientSocket,"PASV")
port = builtport(message)
dataSocket = socket(AF_INET, SOCK_STREAM)
dataSocket.connect((serverName, port))
message = send(clientSocket,"LIST")
message = dataSocket.recv(2048)
print message
message = clientSocket.recv(2048)
print message

#DOWNLOAD FILE FROM NEW PUBLIC DIRECTORY
message = send(clientSocket,"CWD amr")
message = send(clientSocket,"PASV")
port = builtport(message)
dataSocket = socket(AF_INET, SOCK_STREAM)
dataSocket.connect((serverName, port))

message = send(clientSocket,"RETR 20160513104000_0695.dat")
start = message.find("(")
end  = message.find(")")
byteNum = message[start+1:end].split()[0]
print byteNum

#Loop until all bytes are recieved.
while byteNum > 0:
	message = dataSocket.recv(2048)
	print message
	byteNum = int(byteNum) - len(message)

message = clientSocket.recv(2048)
print message

time.sleep(2)
dataSocket.close()
message = send(clientSocket,"QUIT")
clientSocket.close()
