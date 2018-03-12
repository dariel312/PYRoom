class ChatClient(object):
	def __init__ (self, socket, name):
		self.socket = socket
		self.name = name
		self.thread = None

	def send(self, message):
		self.socket.send(message.encode('utf8'))

	def receive(self, size=4096):
		return self.socket.recv(size).decode('utf8')