
import socket
import sys
import threading
import uuid
from Const import *
from ChatClient import *
from Channel import *
from User import *

class Server:
	SERVER_CONFIG = {
		"MAX_CONNECTIONS": 15,
		"SERVER_NAME": "Dariel's Chat",
		"VERSION": "1.0",
		"DB_PATH": "./"
	}
	BANNER = ""

	def __init__(self, host=socket.gethostbyname('localhost'), port=50000, allowReuseAddress=True):
		self.host = host
		self.port = port
		self.address = (self.host, self.port)
		self.clients = {}
		self.clientThreadList = []
		self.channels = {} # Channel Name -> Channel

		self.BANNER = open("banner.txt").read()

		try:
			self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except socket.error as errorMessage:
			sys.stderr.write("Failed to initialize the server. Error - %s\n", errorMessage[1])
			raise

		if allowReuseAddress:
			self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		try:
			self.serverSocket.bind(self.address)
		except socket.error as errorMessage:
			sys.stderr.write('Failed to bind to ' + self.address + '. Error - %s\n', errorMessage[1])
			raise

	def listen_thread(self):
		#listener loop
		while True:
			print("Waiting for a client to establish a connection\n")
			clientSocket, clientAddress = self.serverSocket.accept()
			print("Connection established with IP address {0} and port {1}\n".format(clientAddress[0], clientAddress[1]))
					
			clientThread = threading.Thread(target=self.client_thread, args=(clientSocket, clientAddress))
			
			self.clientThreadList.append(clientThread)
			clientThread.start()

		#if we exit this while loop then were no longer accepting connections
		for thread in self.clientThreadList:
			if thread.is_alive():
				thread.join()

	def start_listening(self):
		self.serverSocket.listen(Server.SERVER_CONFIG["MAX_CONNECTIONS"])
		listenerThread = threading.Thread(target=self.listen_thread)
		listenerThread.start()
		listenerThread.join()

	def client_thread(self, clientSocket, clientAddress, size=4096):
	
		#add user to list
		client = ChatClient(clientSocket, uuid.uuid4())
		self.clients[client.uid] = client
	
		#send greeting get name
		client.send(self.BANNER)
		client.send(Const.WELCOME_INITIAL)
		self.send_server_name(client) #sets the client the server name (Meta)

		#send welcome message
		welcomeMessage = Const.WELCOME_MESSAGE % client.name
		client.send(welcomeMessage)

		#handler loop
		while True:
			chatMessage = client.receive()
			params = chatMessage.split(' ')
			op = params[0].lower()

			if op == '/quit':
				self.quit(client)
				break
			elif op == '/list':
				self.list_all_channels(client)
			elif op == '/ping':
				self.ping(client, " ".join(params[1:]))
			elif op == '/nick':
				self.nick(client, params)
			elif op == '/help':
				self.help(client)
			elif op == '/join':
				self.join(client, chatMessage)
			elif op == '/version':
				self.version(client)

			elif op == '/away':
				self.away(client)
			else:
				self.send_message(client, chatMessage)

	def server_shutdown(self):
		print("Shutting down chat server.\n")
		self.serverSocket.shutdown(socket.SHUT_RDWR)
		self.serverSocket.close()

	def get_user_channel(self, client):
		for chnl in self.channels.values():
			if client.uid in chnl.clients: #returns first occurence of user in channel
				return chnl
		return None

	def send_server_name(self, client):
		client.send("/servername " + self.SERVER_CONFIG["SERVER_NAME"])
	
	def load_users(self):
		text = open(self.SERVER_CONFIG["DB_PATH"] + "users.txt").read()
		users = []
		for line in text.split("\n"):
			if line == "": continue

			params = line.split(' ')
			usr = User()
			usr.uid = params[0]
			usr.name = params[1]
			usr.password = params[2]
			usr.role = params[3]
			users.append(usr)
		return users

	#handlers
	def send_message(self, client, chatMessage):
		usrChnl = self.get_user_channel(client)

		if usrChnl != None: #if user is in channel broadcast
			usrChnl.broadcast_message(chatMessage, client)
		else:
			client.send(Const.NOT_CHANNEL_MESSAGE)

	def join(self, client, chatMessage):
		isInSameRoom = False

		 #handle error
		if len(chatMessage.split()) != 2:
			self.help(client)
			return 

		channelName = chatMessage.split()[1]
		usrChnl = self.get_user_channel(client)
		targetChnl = self.channels.get(channelName)

		#create channel if doesnt exist
		if targetChnl == None:
			targetChnl = Channel(channelName)
			self.channels[channelName] = targetChnl

		#if user is in channel
		if usrChnl == targetChnl:
			client.send(Const.ALREADY_IN_CHANNEL + channelName)
		else:
			if usrChnl != None: #removes him from old channel
				usrChnl.remove_client(client)
			targetChnl.add_client(client)

	def version(self, client):
		client.send("\n> Version: " + self.SERVER_CONFIG["VERSION"])

	def nick(self, client, params):
		users = self.load_users()

		if len(params) is not 2: #if user didnt put param
			self.help(client)
			return

		name = params[1]

		if name in [user.name for user in users]: #name is taken
			client.send(Const.USER_TAKEN)
			return

		oldName = client.name
		client.name = name
		client.send("> Nickname changed to " + name)
		chnl = self.get_user_channel(client)

		#notify users in channel of new name
		if chnl != None:
			for c in chnl.clients.values():
				if c is not client:
					c.send(Const.CHANGED_NAME.format(oldName, client.name))


	def away(self, client, message):
		client.set_away(True, message)

	def info(self, client):
		client.send(Const.INFO)

	def quit(self, client):
		#remove from channel
		channel = self.get_user_channel(client)
		if channel != None:
			channel.remove_client(client)

		#disconnect
		client.send(Const.DISCONNECTED)
		client.send('/quit')
		print("Connection with IP address {0} has been removed.\n".format(client.socket.getsockname()))
		client.close()
		del self.clients[client.name]

	def list_all_channels(self, client):
		channelsNames = [chnl.name + " ({0})".format(len(chnl.clients)) for chnl in self.channels.values()]

		if len(channelsNames) == 0:
			msg = Const.NO_CHANNELS
		else:
			msg = Const.LIST_ALL_CHANNELS + ", ".join(channelsNames) + "\n"

		client.send(msg)

	def list_all_users(self, client, name=''):
		message = Const.LIST_ALL_USERS
		users_list = ["You" if client.name == name else client.name for client in self.clients.values()]
		message = message + ", ".join(users_list) + "\n"
		client.send(message)

	def ping(self, client, message):
		client.send("> PONG " + message)

	def help(self, client):
		client.send(Const.HELP_MESSAGE)


def main():
    chatServer = Server()
    print("\nListening on port " + str(chatServer.port))
    print("Waiting for connections...\n")

    chatServer.start_listening()
    chatServer.server_shutdown()

if __name__ == "__main__":
    main()
