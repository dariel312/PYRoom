from Const import Const

class Channel:
	def __init__(self, name):
		self.clients = {} # Client Name -> Socket
		self.name = name

	def add_client(self, client):
		self.clients[client.uid] = client
		self.welcome_client(client)

	def welcome_client(self, client):
		for c in self.clients.values():
			if c.name is client.name:
				chatMessage = '> {0} have joined the channel {1}!'.format("You", self.name)
				c.send(chatMessage + "\n" + Const.CHANNEL_USER_COUNT.format(len(self.clients)))
			else:
				chatMessage = '> {0} has joined the channel {1}!'.format(client.name, self.name)
				c.send(chatMessage)

	#sends a message to all users in channel as a user
	def broadcast_message(self, message, senderClient):
		for client in self.clients.values():
			if client.name != senderClient.name:
				client.send(senderClient.name + ": " + message)
			else:
				client.send('You: ' + message)

	def send_to_all(self, message):
		for client in self.clients.values():
			client.send(message)

	def remove_client(self, client):
		del self.clients[client.uid]
		leave_message = ">" + client.name + " has left the channel " + self.name
		self.send_to_all(leave_message)
