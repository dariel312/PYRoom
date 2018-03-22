import wpf
from System import TimeSpan
from System.Windows.Controls import *
from System.Windows import *
from System.Windows.Threading import *
from System.Windows.Input import *
from ConnectPrompt import *
from ViewModels import *
from Client import *
import socket
import sys
import threading

class WindowMain(Window):

	def __init__(self):
		self.ui = wpf.LoadComponent(self, 'WindowMain.xaml')
		self.sidebar = self.ui.sidebar
		self.model = AppVM() #object to which UI thread and socket thread will communicate
		self.client = Client()

		#setup ui threadupdate
		self.updater = DispatcherTimer()
		self.updater.Tick += self.update_UI
		self.updater.Interval = TimeSpan(0,0,0,0,33)
		self.updater.Start()


	def update_UI(self, sender, e):
		"""updates ui for data changes"""

		if self.model.currentChannel == None: #update messages b4 youre in channel
			self.ui.messages.Text = self.model.messages
		else:
			self.ui.messages.Text = self.model.currentChannel.messages

		self.ui.serverName.Content = self.model.serverName
		self.ui.Title = self.model.serverName

		#update message box
		if self.model.isNewMessage:
			self.messages.ScrollToEnd()
			self.model.isNewMessage = False
		
		#uodate channel queue
		for channelOP in self.model.channelQueue:
			if channelOP.op == "add":
				item = ListBoxItem()
				item.Content = "{0}".format(channelOP.name)
				self.ui.channels.Items.Add(item)
				self.model.channels[channelOP.name].listbox = item
			elif channelOP.op == "delete":
				pass
			elif channelOP.op == "message":
				self.model.channels[channelOP.name].messages += channelOP.message + '\n'

				if channelOP.name == self.model.currentChannel.name:
					self.model.messages += channelOP.message + "\n"
					self.model.isNewMessage = True

			self.model.channelQueue.remove(channelOP)
				
		#update ui if we got a channel
		if self.ui.channels.SelectedItem == None and self.model.currentChannel != None:
			self.ui.channels.SelectedItem = self.model.currentChannel.listbox

		#update UI if we changed channels
		if self.model.currentChannel != None:
			if self.model.currentChannel.name != self.ui.channels.SelectedItem.Content:
				self.ui.channels.SelectedItem = self.model.currentChannel.listbox

	#GUI STUFF
	def MyMessage_KeyDown(self, sender, e):
		if e.Key == Key.Return:
			self.submit_message(self.ui.myMessage.Text)

	def SideBar_ToggleClick(self, sender, e):
		if (self.sidebar.Visibility == Visibility.Collapsed):
			self.sidebar.Visibility = Visibility.Visible
		else:
			self.sidebar.Visibility = Visibility.Collapsed

	def Send_Click(self, sender, e):
		self.submit_message(self.ui.myMessage)

	def Menu_Click(self, sender, e):
		sender.ContextMenu.IsOpen = True
	
		
	def Menu_Connect_Click(self, sender, e):
		prompt = ConnectPrompt()
		prompt.ShowDialog()
		if prompt.result:
			self.submit_message("/connect {0} {1}".format(prompt.host, prompt.port))
		
	def channels_SelectionChanged(self, sender, e):
		newName = sender.SelectedItem.Content
		if  self.model.currentChannel == None or newName!= self.model.currentChannel.name: #if user click diff channel change model chnl
			if self.model.currentChannel.joined: #only sendif havent joined yet
				self.send_message("/join " + newName)
			self.model.currentChannel = self.model.channels.get(newName)
		self.model.messages = self.model.currentChannel.messages

	def Menu_Exit_Click(self, sender, e):
		self.close()
	
	#CLIENT STUFF
	def close(self): 
		"""used to close form GUI events not from console"""
		self.submit_message("/quit")

	
	def submit_message(self, message):
		"""submits message from text box."""
		self.handle_send_command(message)
		self.ui.myMessage.Text = ''

	
	def send_message(self, message):
		"""sends message to server"""
		self.client.send(message + "\r\n")


	def handle_send_command(self, msg):
		"""intercepts send commands and dispatches them """
		params = msg.split(' ')
		op = params[0].lower()

		if op == '/connect' and not self.client.isClientConnected:
			self.connect(params)
		if op == '/quit':
			self.send_message("/quit")
			self.client.disconnect()
		else:
			self.send_message(msg)

	def client_thread(self):
		while self.client.isClientConnected:
			#get data from socket
			try:
				data = self.client.receive()
			except:
				print("Fail silently: Socket disconnected")
				break

			commands = filter(None, data.split("\r\n"))

			for command in commands:
				#handle commands from serv
				params = command.split(' ')
				op = params[0]
				if op == '/servername':
					self.recv_server_name(" ".join(params[1:]))
				elif op == '/joined':
					self.model.currentChannel = self.model.channels.get(params[1])
					self.model.currentChannel.joined = True
				elif op == '/channel':
					cOP = ChannelOP(params[1], params[2])

					if cOP.op == 'message': #message param only for when op = message
						cOP.message = ' '.join(params[3:])
					elif cOP.op == 'add':
						self.model.channels[cOP.name] = ChannelVM(cOP.name, None)

					self.model.channelQueue.append(cOP)

				else:
					if self.model.currentChannel == None: #add to base str
						self.model.messages += command + "\n"
					else: #now were in channel add to channel str
						self.model.currentChannel.messages += command + "\n"
					self.model.isNewMessage = True

	#SEND handlers
	def connect(self, params):
		if len(params) is not 3:
			return

		self.client = Client()
		try:
			self.client.connect(host = params[1], port=int(params[2]))
			self.clientThread = threading.Thread(target=self.client_thread)
			self.clientThread.start()
		except:
			MessageBox.Show("Failed to connect to {0}:{1}".format(params[1], params[2]))

	#RECV HANDLERS
	def recv_server_name(self, name):
		self.model.serverName = name