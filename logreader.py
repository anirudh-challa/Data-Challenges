import socket
import sys

import SocketServer

class MyTCPHandler(SocketServer.BaseRequestHandler):
	"""
	The request handler class for our server.

	It is instantiated once per connection to the server, and must
	override the handle() method to implement communication to the
	client.
	"""

	def handle(self):
		# self.request is the TCP socket connected to the client
		self.data = self.request.recv(1024).strip()
		
		accept(self.data) 
		

	

def accept(data):

	
	field_dict = {}
	lines = data.split('\n')
		#print req_dict
	try:
		for line in lines:
			fields = line.split(',')
			for field in fields:
				key = field.split('=')[0]
				value = field.split('=')[1]
				field_dict[key] = value

			flag = 0
			
			for key in req_dict.keys():
				if req_dict[key] != field_dict[key]:
					flag = 1 

			if flag == 0:
				print line

	except (AttributeError, IndexError, KeyError):
		print "There is an error in the input", line
		pass


	return





if __name__ == '__main__':

	ip = sys.argv[1]
	port = int(sys.argv[2])
	reqs = sys.argv[3]

	global req_dict
	req_dict = {}
	reqs = reqs.split(',')
	for req in reqs:
		key = req.split('=')[0]
		value = req.split('=')[1]
		req_dict[key] = value

	#print req_dict	


	server = SocketServer.TCPServer((ip, port), MyTCPHandler)
	
	server.serve_forever()

	#data = s.recv(BUFFER_SIZE)

	#print data
	