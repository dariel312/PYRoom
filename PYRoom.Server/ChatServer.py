
import socket
import sys
import threading
import uuid
import json
import datetime
from Const import *
from ChatClient import *
from Channel import *
from User import *

class ChatServer:
	SERVER_CONFIG = {
		"MAX_CONNECTIONS": 15,
		"SERVER_NAME": "Dariel's Chat",
		"VERSION": "1.0",
	}
	BANNER = ""

	def __init__(self, host=socket.gethostbyname('localhost'), port=50000, allowReuseAddress=True, dbPath = "./"):
		self.host = host
		
		self.port = port
		if self.port is None:
			self.port = 50000
		
		self.dbPath = dbPath
		if self.dbPath is None:
			self.dbPath = "./"

		self.address = (self.host, self.port)
		self.clients = {}
		self.clientThreadList = []
		self.channels = {} # Channel Name -> Channel
		self.stopLisening = False

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

	def load_channels(self):
		file = open(self.dbPath + "/channels.json").read()
		#self.channels = 

	def listen_thread(self):
		#listener loop
		while not self.stopLisening:
			print("Waiting for a client to establish a connection\n")
			try:
				clientSocket, clientAddress = self.serverSocket.accept()
			except:
				break
			print("Connection established with IP address {0} and port {1}\n".format(clientAddress[0], clientAddress[1]))
					
			clientThread = threading.Thread(target=self.client_thread, args=(clientSocket, clientAddress))
			
			self.clientThreadList.append(clientThread)
			clientThread.start()

		#if we exit this while loop then were no longer accepting connections
		for thread in self.clientThreadList:
			if thread.is_alive():
				thread.join()

	def start_listening(self):
		self.serverSocket.listen(ChatServer.SERVER_CONFIG["MAX_CONNECTIONS"])
		self.listenerThread = threading.Thread(target=self.listen_thread)
		self.listenerThread.start()
		self.stopLisening = False

	def client_thread(self, clientSocket, clientAddress, size=4096):
	
		#add user to list
		client = ChatClient(clientSocket, uuid.uuid4())
		self.clients[client.uid] = client
	
		#send greeting
		client.send(self.BANNER)
		client.send(Const.WELCOME_INITIAL)
		client.send(Const.WELCOME_MESSAGE % client.name)
		client.send(Const.RULES)
		self.send_server_name(client) #sets the client the server name (Meta)
		self.send_gui_channels(client) #sets channel list (meta)

		#handler loop
		while not client.closed:
			try:
				chatMessage = client.receive()
			except:
				print("Error recieving from socket, client {0}. Client likely disconnected.".format(client.name))
				break

			commands = filter(None, chatMessage.split("\r\n"))
			
			#could be multiple commands in one receive
			for command in commands:
				params = command.split(' ')
				op = params[0].lower()

				if op == '/quit':
					self.quit(client)
					break
				elif op == '/list':
					self.list_all_channels(client)
				elif op == '/info':
					self.info(client)
				elif op == '/ping':
					self.ping(client, " ".join(params[1:]))
				elif op == '/nick':
					self.nick(client, params)
				elif op == '/help':
					self.help(client)
				elif op == '/invite':
					self.invite(client, params)
				elif op == '/userhost':
					self.user_host(client, params)
				elif op == '/userip':
					self.user_host(client, params)
				elif op == '/users':
					self.users(client)
				elif op == '/user':
					self.user(client)
				elif op == '/join':
					self.join(client, chatMessage)
				elif op == '/version':
					self.version(client)
				elif op == '/privmsg':
					self.private_message(client, params)
				elif op == '/notice':
					self.private_message(client, params, useAutoReply = False)
				elif op == '/away':
					self.away(client, params)
				elif op == '/kick':
					self.kick(client, params)
				elif op == '/topic':
					self.topic(client, params)
				elif op == '/ison':
					self.ison(client, params)
				elif op == '/rules':
					self.rules(client)
				elif op == '/die':
					self.die(client) 
				elif op == '/restart':
					self.restart(client)
				elif op == '/oper':
					self.oper(client, params)
				elif op == '/time':
					self.time(client)
				elif op == '/whois':
					self.whois(client, params)
				elif op == '/setname':
					self.set_name(client, params)
				elif op == '/silence':
					self.silence(client, params)
				elif op == '/message':
					self.message(client, params) 
				else: #removed since user doesnt have a default channel
					self.help(client)

	def set_restart_callback(callback):
		pass

	def server_shutdown(self):
		print("Shutting down chat server.\n")

		self.stopLisening = True 
		for client in self.clients.values():
			client.send(Const.SHUTTING_DOWN)
			client.socket.close()

		self.serverSocket.close()
		
	def load_config(self):
		pass

	def get_user_with_name(self, name):
		for client in self.clients.values():
			if client.name == name:
				return client
		return None

	def get_user_channel(self, client):
		"""Returns the current channel the user is in (Deprecated)"""
		for chnl in self.channels.values():
			if client.uid in chnl.clients: #returns first occurence of user in channel
				return chnl
		return None

	def get_user_channels(self, client):
		"""Returns a list of channels the user is in"""
		channels = []
		for chnl in self.channels.values():
			if client.uid in chnl.clients:
				channels.append(chnl)
		return channels

	def send_gui_channels(self, client):
		for channel in self.channels.values():
			client.send("/channel add {0} {1}".format(channel.name, len(channel.clients)))

	def send_server_name(self, client):
		client.send("/servername " + self.SERVER_CONFIG["SERVER_NAME"])
	
	def load_users(self):
		text = open(self.dbPath + "users.txt").read()
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

	def login_user(self, username, password):
		users = self.load_users()
		for user in users:
			if user.name == username and user.password == password:
				return user
		return None

	def add_channel(self, channelName):
		targetChnl = Channel(channelName)
		self.channels[channelName] = targetChnl

		#send update
		for client in self.clients.values():
			client.send("/channel add {0}".format(targetChnl.name))

		return targetChnl

	#handlers
	#def send_message(self, client, chatMessage):
	#	""" Sends message to users current channel (Deprecated)"""
	#	usrChnl = self.get_user_channel(client)

	#	if client.isSilenced:
	#		client.send("> You are silenced.")
	#		return

	#	if usrChnl is not None: #if user is in channel broadcast
	#		usrChnl.broadcast_message(chatMessage, client)
	#	else:
	#		client.send(Const.NOT_CHANNEL_MESSAGE)

	def user_host(self, client, params):
		for username in params[1:]:
			user = self.get_user_with_name(username)
			client.send("> {0}: {1}".format(user.name, user.socket.getsockname()))

	def rules(self, client):
		client.send(Const.RULES)

	def message(self, client, params):
		channelName = params[1]
		message = ' '.join(params[2:])

		channel = self.channels.get(channelName)
		if channel != None:
			channel.broadcast_message(message, client)


	def oper(self, client, params):
		if len(params) is not 3:
			self.help(client)
			return
	
		username = params[1]
		password = params[2]

		users = self.load_users()
		user = self.login_user(username, password)

		if user is not None and (user.role == 'sysop' or user.role=='admin'):
			client.isOperator = True
			client.isLoggedIn = True
			client.username = user.name
			client.role = user.role
			client.send("> Logged in successfully.")
		else:
			client.send("> Invalid username or password.")
	
	def silence(self, client, params):
		if not client.isOperator:
			client.send(Const.MUST_BE_OP)
			return
		
		for c in self.clients.values():
			c.isSilenced = not c.isSilenced

		client.send("")

	def set_name(self, client, params):
		if len(params) < 2:
			self.help(client)
			return

		name = " ".join(params[1:])
		client.realName = name
		client.send(Const.SETNAME_SUCCESS.format(name))

	def users(self, client):
		for user in self.clients.values():
			channels = self.get_user_channels(user)
			chnlStr = ''

			if len(channels) == 0:
				chnlStr = "None"
			else:
				chnlStr = ', '.join([c.name for c in channels]) #only thing I like about python

			client.send("> Nick: {0}\tChannel(s): {1}".format(user.name, chnlStr))

	def whois(self, client, params):
		for name in params[1:]:
			tUser = self.get_user_with_name(name)
			channels = self.get_user_channels(tUser)

			if len(channels) == 0:
				chnlStr = "None"
			else:
				chnlStr = ', '.join([c.name for c in channels])

			client.send(Const.WHO_IS.format(tUser.name, tUser.realName, tUser.isAway, tUser.isLoggedIn, chnlStr))

	def private_message(self, client, msgParams, useAutoReply=True):

		if len(msgParams) < 3: #error checks
			self.help(client)
			return

		targetName = msgParams[1]
		msg = msgParams[2:]

		target = self.get_user_with_name(targetName)
		
		if target is None: #target not found
			client.send(Const.MSG_USER_NOT_FOUND.format(targetName))
			return

		client.send("You > {0}: {1}".format(targetName, ' '.join(msg)))
		target.send("{0} > You: {1}".format(client.name, ' '.join(msg)))

		if target.isAway and useAutoReply:
			client.send("> {0} is away with message: {1}".format(target.name, target.awayMessage))
	
	def die(self, client):
		if client.isOperator is False:
			client.send(Const.MUST_BE_OP)
			return
		
		self.server_shutdown()

	def restart(self):
		if client.isOperator is False:
			client.send(Const.MUST_BE_OP)
			return
		
		self.server_shutdown()
		self.restartCallBack()


	def user(self, client, params):
		if len(params) != 2:
			self.help(client)
		
		client.username = params[1]


	def invite(self, client, params):
		if len(params) is not 3:
			self.help(client)
			return

		targetName = params[1]
		channelName = params[2]

		target = self.get_user_with_name(targetName)

		if target is None:
			client.send("> User not found")

		targetChannel = self.channels.get(channelName)
		userChannels = self.get_user_channels(target)

		if targetChannel is None: #if doesnt exist add it
			targetChannel = Channel(targetChannel)
			self.channels[channelName] = targetChannel

		for usrChn in userChannels:
			if usrChn is targetChannel: #user already in channel
				client.send(Const.ALREADY_IN_CHANNEL + channelName)
				return

		targetChannel.add_client(target)
		client.send("> {0} has been added to {1}.".format(targetName, channelName))

	def join(self, client, chatMessage):
		isInSameRoom = False

		 #handle error
		if len(chatMessage.split()) != 2:
			self.help(client)
			return 

		channelName = chatMessage.split()[1]
		usrChnls = self.get_user_channels(client)
		targetChnl = self.channels.get(channelName)

		#create channel if doesnt exist
		if targetChnl == None:
			targetChnl = self.add_channel(channelName)

		#if user is in channel
		for chn in usrChnls:
			if chn is targetChnl:
				client.send(Const.ALREADY_IN_CHANNEL + channelName)
				return
		
		#add him to channel if nothing fails
		targetChnl.add_client(client)
		client.send("/joined " + targetChnl.name)


	def topic(self, client, params):
		if len(params) < 2:
			self.help(client)
			return

		chnnl = self.channels.get(params[1])

		if chnnl is None:
			client.send("> Channel does not exist.")
			return 

		if len(params) > 2:#set topic
			topic = ' '.join(params[2:])
			chnnl.set_topic(topic)
		else: #send topic
			client.send("> Topic: " + chnnl.topic)


	def kick(self, client, params):
		if not client.isoperator:
			client.send(const.must_be_op)
			return
		
		if len(params) is not 3:
			self.help(client)
			return

		trget = self.get_user_with_name(params[2])
		usrChnl = self.get_user_channel(trget) #FIX
		trgChnl = self.channels.get(params[1])
		
		if usrChnl is None or usrChnl != trgChnl:
			client.send("> User not in that channel.")
			return

		trgChnl.remove_client(client)
		client.send("> You have been kicked from the channel.")

	def version(self, client):
		client.send(Const.SERVER_VERSION.format(self.SERVER_CONFIG["VERSION"]))

	def ison(self, client, params):
		users = []

		#get users
		for name in params[1:]:
			user = self.get_user_with_name(name)
			if user is not None:
				users.append(user.name)

		client.send(Const.IS_ON.format(" ".join(users)))

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
		chnls = self.get_user_channels(client)

		#notify users in channel of new name
		for chn in chnls:
			chn.notify_nick_change(client, oldName)


	def away(self, client, params):
		if len(params) is 1:
			client.set_away(False)
			client.send("> You are not AWAY.")
		else:
			message = " ".join(params[1:])
			client.set_away(True, message)
			client.send("> You are AWAY.")


	def info(self, client):
		client.send(Const.INFO)

	def time(self, client):
		dt = datetime.datetime.now()
		client.send("> Time:" + dt.strftime('%Y-%m-%d %H:%M:%S'))

	def quit(self, client):
		#remove from channel
		chnls = self.get_user_channels(client)
		for chnl in chnls:
			chnl.remove_client(client)
		#disconnect
		client.send(Const.DISCONNECTED)
		#client.send('/quit')
		print("Connection with IP address {0} has been removed.\n".format(client.socket.getsockname()))
		client.close()
		del self.clients[client.uid]

	def list_all_channels(self, client):
		channelsNames = [chnl.name + " ({0})".format(len(chnl.clients)) for chnl in self.channels.values()]

		if len(channelsNames) == 0:
			msg = Const.NO_CHANNELS
		else:
			msg = Const.LIST_ALL_CHANNELS + ", ".join(channelsNames)

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
