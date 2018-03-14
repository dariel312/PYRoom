class ChatClient(object):
	def __init__ (self, socket, uid):
		self.socket = socket
		self.uid = str(uid)
		self.name = "anonymous#" + ''.join(self.uid[0:8])
		self.thread = None
		self.isAway = False
		self.awayMessage = ""
		self.isLoggedIn = False
		self.closed = False

	def set_away(self, isAway, message = ''):
		self.isAway = isAway
		self.awayMessage = message

	def send(self, message):
		self.socket.send((message + "\r\n").encode('utf8'))

	def receive(self, size=4096):
		return self.socket.recv(size).decode('utf8')

	def close(self):
		self.closed = True
		self.socket.close()