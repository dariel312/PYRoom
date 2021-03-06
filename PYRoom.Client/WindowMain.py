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

	def __init__(self, host = None, port = None, testFile = None):
		self.ui = wpf.LoadComponent(self, 'WindowMain.xaml')
		self.sidebar = self.ui.sidebar
		self.model = AppVM() #object to which UI thread and socket thread will communicate
		self.client = Client()

		#setup ui threadupdate
		self.updater = DispatcherTimer()
		self.updater.Tick += self.update_UI
		self.updater.Interval = TimeSpan(0,0,0,0,33)
		self.updater.Start()

		if host != None and port != None:
			p = int(port)
			h = str(host)
			self.submit_message("/connect {0} {1}".format(h,p))

		#run test script
		if testFile != None:
			try:
				file = open(testFile)
				text = file.read()
				lines = text.split("\n")
				for line in lines:
					self.submit_message(line)
				MessageBox.Show("Test file has been run.")
			except:
				MessageBox.Show("Failed to open " + testFile)

	def update_UI(self, sender, e):
		"""updates ui for data changes"""

		if self.model.currentChannel == None: #update messages b4 youre in channel
			self.ui.messages.Text = self.model.messages
		else:
			self.ui.messages.Text = self.model.currentChannel.messages

		self.ui.serverName.Content = self.model.serverName
		self.ui.windowTitle.Content = self.model.serverName
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



				if self.model.currentChannel != None and channelOP.name == self.model.currentChannel.name:
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
		self.submit_message(self.ui.myMessage.Text)

	def Menu_Click(self, sender, e):
		sender.ContextMenu.IsOpen = True

	def Minimize_Click(self, sender, e):
		self.WindowState = WindowState.Minimized

	def Maximize_Click(self, sender, e):
		if self.WindowState == WindowState.Normal:
			self.WindowState = WindowState.Maximized
		else:
			self.WindowState = WindowState.Normal

	def Exit_Click(self, sender, e):
		self.close()

	def Rectangle_MouseDown(self, sender, e):
		if(e.ChangedButton == MouseButton.Left):
			if(self.WindowState == WindowState.Maximized):
				self.WindowState = WindowState.Normal
			self.DragMove()
		
	def Menu_Connect_Click(self, sender, e):
		prompt = ConnectPrompt()
		prompt.ShowDialog()
		if prompt.result:
			self.submit_message("/connect {0} {1}".format(prompt.host, prompt.port))

	def Menu_ClearChat_Click(self, sender, e):
		self.clear_chatbox()
	
	def channels_SelectionChanged(self, sender, e):
		newName = sender.SelectedItem.Content
		if  self.model.currentChannel == None or newName!= self.model.currentChannel.name: #if user click diff channel change model chnl
			if  self.model.currentChannel == None or not self.model.channels[newName].joined: #only sendif havent joined yet
				self.send_command("/join " + newName)
			self.model.currentChannel = self.model.channels.get(newName)
		self.model.messages = self.model.currentChannel.messages
		self.model.isNewMessage = True #scroll to bottonm now
	def Menu_Exit_Click(self, sender, e):
		self.close()
	
	#CLIENT STUFF
	def close(self): 
		"""used to close form GUI events not from console"""
		self.submit_message("/quit")

	def clear_chatbox(self):
		"""Clears chat window, cleans it out"""
		if self.model.currentChannel == None: #update messages b4 youre in channel
			self.model.messages = ""
		else:
			self.model.currentChannel.messages = ""

	def submit_message(self, message):
		"""submits message from text box."""
		self.handle_send_command(message)
		self.ui.myMessage.Text = ''

	
	def send_message(self, params):
		"""sends message to server"""
		message = " ".join(params)
		self.client.send("/message {0} {1}\r\n".format(self.model.currentChannel.name, message))

	def send_command(self, message):
		"""sends command to server"""
		self.client.send(message + "\r\n")

	def handle_send_command(self, msg):
		"""intercepts send commands and dispatches them """
		params = msg.split(' ')
		op = params[0].lower()

		if len(msg) == 0:
			return #pressed enter with no msg typed

		if op == '/connect' and not self.client.isClientConnected:
			self.connect(params)
		elif op == '/quit':
			self.send_message("/quit")
			self.client.disconnect()
		elif list(msg)[0] == '/':
			self.send_command(msg)
		elif self.model.currentChannel is not None:
			self.send_message(params)

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