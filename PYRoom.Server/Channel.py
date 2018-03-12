

class Channel:
	def __init__(self, name):
		self.clients = {} # Client Name -> Socket
		self.name = name

	def add_client(self, client):
		self.clients[client.name] = client
		self.welcome_client(client)

	def welcome_client(self, client):
		for c in self.clients.values():
			if c.name is client.name:
				chatMessage = '\n> {0} have joined the channel {1}!\n'.format("You", self.name)
				c.send(chatMessage)
			else:
				chatMessage = '\n> {0} has joined the channel {1}!\n'.format(client.name, self.name)
				c.send(chatMessage)
				
	#sends a message to all users in channel as a user
	def broadcast_message(self, message, senderClient = None):
		for client in self.clients.values():
			if senderClient == None or client.name != senderClient.name:
				client.send(senderClient.name + ": " + message)
			else:
				client.send('You: ' + message)

	def remove_client_from_channel(self, clientName):
		del self.clients[clientName]
		leave_message = "\n" + clientName + " has left the channel " + self.name + "\n"
		self.broadcast_message(leave_message)
