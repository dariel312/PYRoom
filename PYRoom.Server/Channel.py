from Const import Const

class Channel:
	def __init__(self, name):
		self.clients = {} # Client Name -> Socket
		self.name = name
		self.topic = 'None'

	def add_client(self, client):
		self.clients[client.uid] = client
		self.welcome_client(client)

	def welcome_client(self, client):
		for c in self.clients.values():
			if c.name is client.name:
				chatMessage = '/channel message {0} > You have joined the channel {1}!'.format(self.name, self.name)
				chatMessage += "\n> Channel Topic: " + self.topic
				chatMessage += "\n" + Const.CHANNEL_USER_COUNT.format(len(self.clients))
				c.send(chatMessage)
			else:
				chatMessage = '/channel message {0} > {1} has joined the channel {2}!'.format(self.name, client.name, self.name)
				c.send(chatMessage)

	#sends a message to all users in channel as a user
	def broadcast_message(self, message, senderClient):
		for client in self.clients.values():
			if client.name != senderClient.name:
				client.send("/channel message {0} {1}: {2}".format(self.name, senderClient.name, message))
			else:
				client.send('/channel message {0} You: {1}'.format(self.name, message))

	def send_to_all(self, message):
		for client in self.clients.values():
			client.send(message)

	def remove_client(self, client):
		del self.clients[client.uid]
		leave_message = "/channel message {0} > {1} has left the channel {2}".format(self.name, client.name, self.name)
		self.send_to_all(leave_message)

	def set_topic(self, topic):
		self.topic = topic
		self.send_to_all("/channel message {0} > Topic has been changed to: {1}".format(self.name, topic))

	def notify_nick_change(self, client, oldName):
		for c in self.clients.values():
			if c is not client:
				c.send("/channel message {0} ".format(self.name) + Const.CHANGED_NAME.format(oldName, client.name))

	def notify_invite(self, inviter, invitee):
		for c in self.clients.values():
			c.send("/channel message {0} > {1} has invited {2} to this channel.".format(self.name, inviter.name, invitee.name))

