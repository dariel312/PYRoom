
import socket
import sys
import threading
from Const import *
from ChatClient import *
from Channel import *

class Server:
	SERVER_CONFIG = {"MAX_CONNECTIONS": 15}

	def __init__(self, host=socket.gethostbyname('localhost'), port=50000, allowReuseAddress=True):
		self.host = host
		self.port = port
		self.address = (self.host, self.port)
		self.clients = {}
		self.clientThreadList = []
		self.channels = {} # Channel Name -> Channel

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
		#send greeting get name
		clientSocket.send("> Welcome to our chat app!!! What is your name?\n".encode('utf8'))
		clientName = clientSocket.recv(size).decode('utf8')

		#add user to list
		client = ChatClient(clientSocket, clientName)
		self.clients[clientName] = client

		#send welcome message
		welcomeMessage = Const.WELCOME_MESSAGE % clientName
		client.send(welcomeMessage)

		#handler loop
		while True:
			chatMessage = client.receive()
			params = chatMessage.split(' ')
			op = params[0].lower()

			if op == '/quit':
				self.quit(clientSocket, clientAddress, name)
				break
			elif op == '/list':
				self.list_all_users(client)
			elif op == '/ping':
				self.ping(client, params[1:])
			elif chatMessage == '/help':
				self.help(client)
			elif '/join' in chatMessage:
				self.join(client, chatMessage)
			else:
				self.send_message(client, chatMessage)

	def server_shutdown(self):
		print("Shutting down chat server.\n")
		self.serverSocket.shutdown(socket.SHUT_RDWR)
		self.serverSocket.close()

	def get_user_channel(self, client):
		for chnl in self.channels.values():
			if client.name in chnl.clients: #returns first occurence of user in channel
				return chnl
		return None

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
			targetChnl.add_client(client)


	def quit(self, clientSocket, clientAddress, name=''):
		clientSocket.send('/quit'.encode('utf8'))
		clientSocket.close()
		del self.clients[clientSocket]
		self.broadcast_message(('\n> %s has left the chat room.\n' % name))
		print("Connection with IP address {0} has been removed.\n".format(clientAddress[0]))

	def list_all_users(self, client, name=''):
		message = Const.LIST_ALL_USERS
		users_list = ["You" if client.name == name else client.name for client in self.clients.values()]
		message = message + ", ".join(users_list) + "\n"
		client.send(message)

	def ping(self, client, messageParams):
		client.send(''.join(messageParams))

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
