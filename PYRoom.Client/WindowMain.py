import wpf
from System import TimeSpan
from System.Windows.Controls import *
from System.Windows import *
from System.Windows.Threading import *
from System.Windows.Input import *
from NewChatRoomPrompt import *
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

		self.ui.messages.Text = self.model.messages
		self.ui.serverName.Content = self.model.serverName
		self.ui.Title = self.model.serverName

		if self.model.isNewMessage:
			self.messages.ScrollToEnd()
			self.model.isNewMessage = False

		for channelOP in self.model.channelQueue:
			if channelOP.op is "add":
				pass
			elif channelOP.op is "delete":
				pass

		for userOP in self.model.userQueue:
			if userOP.op is "add":
				pass
			elif userOP.op is "delete":
				pass

	#GUI STUFF
	def MyMessage_KeyDown(self, sender, e):
		if e.Key == Key.Return:
			self.submit_message(self.ui.myMessage.Text)

	def SideBar_ToggleClick(self, sender, e):
		if (self.sidebar.Visibility == Visibility.Collapsed):
			self.sidebar.Visibility = Visibility.Visible
		else:
			self.sidebar.Visibility = Visibility.Collapsed

	def NewRoom_Click(self, sender, e):
		prompt = NewChatRoomPrompt()
		prompt.ShowDialog()
		if prompt.result:
			MessageBox.Show(self.newPrompt.getName())
		else:
			MessageBox.Show("You canceled this new room.") 

	def Send_Click(self, sender, e):
		self.submit_message(self.ui.myMessage)

	def Menu_Click(self, sender, e):
		sender.ContextMenu.IsOpen = True
	
		
	def Menu_Connect_Click(self, sender, e):
		prompt = ConnectPrompt()
		prompt.ShowDialog()
		if prompt.result:
			self.submit_message("/connect {0} {1}".format(prompt.host, prompt.port))
		

	def Menu_Exit_Click(self, sender, e):
		self.cose()
	
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
				break;

			commands =  filter(None, data.split("\r\n"))

			for command in commands:
				#handle commands from serv
				params = command.split(' ')
				op = params[0]
				if op == '/servername':
					self.recv_server_name(" ".join(params[1:]))
				elif op == '/channel':
					self.model.channelQueue.append(ChannelQueue(params[1], params[2]))
				else:
					self.model.messages += command + "\n"
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
