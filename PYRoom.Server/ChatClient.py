class ChatClient(object):
	def __init__ (self, socket, name):
		self.socket = socket
		self.name = name

	def send(self, message):
		self.socket.send(message.encode('utf8'))

	def receive(self):
		return self.socket.recv(size).decode('utf8')