
def parseData (data):
	parsed  = {}
	#Split Data by <cr><lf>
	lines = data.split('\r\n')
	
	#Save Get and File name	
	currentHeader = lines[0].split()
	parsed[currentHeader[0]] = currentHeader[1]

	#Separate each line by header type
	for header in lines:
		try:
			#print header	
			currentHeader = header.split(': ')
			if currentHeader[0].find("GET") >= 0:
				currentHeader = currentHeader[0].split()
			        parsed[currentHeader[0]] = currentHeader[1]

			parsed[currentHeader[0]] = currentHeader[1]

		except IndexError:
			continue
	#Return Dictionary
	return parsed


def printDict (dict):
        count = 1
	for i in dict:
              	print '''Line {0}: {1} | {2}'''.format(count, i, dict[i])
		count = count + 1

#	print sorted(dict)
	return

def fileNotFound (fileName):
	errorLine = "The requested FILE "+ fileName + " was not found on this server."
	sendMessage = '''\
HTTP/1.1 404 Not Found
Date: {0}
Server: Apache
Content-Length: {1}
Connection: close
Content-Type: text

{2}
'''.format(time.strftime("%a, %d %b %Y %X GMT",time.gmtime(time.time())), len(errorLine), errorLine)
	return sendMessage

def ifMod (fileName, reqTime):
	#Get modified time from file, in epoch
	fileTimeSecs =  os.path.getmtime(fileName)
	#Convert epoch to UTC  (GMT)
	filetimeUTC = time.strftime("%a, %d %b %Y %X GMT",time.gmtime(fileTimeSecs))
	print "Modification Time: " + filetimeUTC
	print "Requested Time: " + reqTime
	#Turn strings into timestamps
	fileTimeStamp = datetime.strptime(filetimeUTC,'%a, %d %b %Y %X GMT')
	reqTimeStamp = datetime.strptime(reqTime,'%a, %d %b %Y %X GMT')

	#Compare Timestamps
	if fileTimeStamp > reqTimeStamp:
		print "File needs to be Send again"
		return 1
	else: 
		print "File is Up to Date"	
		
	return 0

def modTime(fileName):
	#Get modified time from file, in epoch
        fileTimeSecs =  os.path.getmtime(fileName)
        #Convert epoch to UTC  (GMT)
        filetimeUTC = time.strftime("%a, %d %b %Y %X GMT",time.gmtime(fileTimeSecs))

	return	filetimeUTC
def fileUpToDate():
	
	sendMessage = '''\
HTTP/1.1 304 Not Modified
Date: {0}
Server: Apache
Connection: close
'''.format(time.strftime("%a, %d %b %Y %X GMT",time.gmtime(time.time())))
	
	return sendMessage

def fileSend (message, length, lastMod):
	sendMessage = '''\
HTTP/1.1 200 OK
Date: {0}
Server: Apache
Last-Modified: {1}
Accept-Ranges: bytes
Content-Length: {2}
Connection: close
Content-Type: text/plain

{3}
'''.format(time.strftime("%a, %d %b %Y %X GMT",time.gmtime(time.time())), lastMod, length, message)
	return sendMessage

from socket import socket, AF_INET, SOCK_STREAM
import sys
import time
import os.path
from datetime import datetime

#Create Server Socket
webServerSocket = socket(AF_INET, SOCK_STREAM)
tcpServerPort = 45793

#Bind tcp Port 
webServerSocket.bind(('', tcpServerPort))
webServerSocket.listen(1)

print "Ready to listen for request on %s" % tcpServerPort
print "Interrupt with CTRL-C"

while True:
	try:
		#Accept connection from client
		#addr is a tuple with port number and ip of client
		print "Waiting for connection"
		webClientSocket, addr = webServerSocket.accept()
		print "Connection on Client IP: %s | Port: %s" % addr

		#Recieve Message
		message = webClientSocket.recv(2048)
		
		#Parse header lines
		headerDict = parseData(message)
		#printDict(headerDict)
		#Get file name and parse it
		fileName = headerDict.get('GET').split('/')[1]	
		
		try:
			#Check if File is up to date
			if ifMod(fileName, headerDict.get('If-modified-since')):
				#open File
				fileObject = open(fileName , "r")
				outMessage = fileObject.read()
				outMessage = fileSend(outMessage, len(outMessage), modTime(fileName))
				webClientSocket.send(outMessage)
			else:
				outMessage = fileUpToDate()
				webClientSocket.send(outMessage)
	
		except (IOError, OSError):
			outMessage = fileNotFound(fileName)
			webClientSocket.send(outMessage)

		#close Client Socket
		webClientSocket.close()
	except KeyboardInterrupt:
		print "Interrupted by CTRL-C"
		break
#Close Web Server Socket
webServerSocket.close()
	


