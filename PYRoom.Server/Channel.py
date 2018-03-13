from Const import Const

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
				chatMessage = '\n> {0} have joined the channel {1}!'.format("You", self.name)
				c.send(chatMessage + "\n" + Const.CHANNEL_USER_COUNT.format(len(self.clients)))
			else:
				chatMessage = '\n> {0} has joined the channel {1}!'.format(client.name, self.name)
				c.send(chatMessage)

	#sends a message to all users in channel as a user
	def broadcast_message(self, message, senderClient = None):
		for client in self.clients.values():
			if senderClient == None or client.name != senderClient.name:
				client.send(senderClient.name + ": " + message)
			else:
				client.send('You: ' + message)

	def remove_client(self, client):
		del self.clients[client.name]
		leave_message = "\n>" + client.name + " has left the channel " + self.name
		self.broadcast_message(leave_message)
