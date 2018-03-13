import wpf
from System import TimeSpan
from System.Windows.Controls import *
from System.Windows import *
from System.Windows.Threading import *
from System.Windows.Input import *
from NewChatRoomPrompt import *
from ViewModels import *
from Client import *
import socket
import sys
import threading

class WindowMain(Window):

	def __init__(self):
		self.ui = wpf.LoadComponent(self, 'WindowMain.xaml')
		self.sidebar = self.ui.sidebar
		self.model = AppVM()
		self.client = Client()

		#setup ui threadupdate
		self.updater = DispatcherTimer()
		self.updater.Tick += self.update_UI
		self.updater.Interval = TimeSpan(0,0,0,0,33)
		self.updater.Start()

		self.isNewMessage = False

	#updates ui for data changes
	def update_UI(self, sender, e):
		self.ui.messages.Text = self.model.messages
		self.ui.serverName.Content = self.model.serverName
		self.ui.Title = self.model.serverName

		if self.isNewMessage:
			self.messages.ScrollToEnd()
			self.isNewMessage = False

	#GUI STUFF
	def MyMessage_KeyDown(self, sender, e):
		if e.Key == Key.Return:
			self.submit_message()

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
		self.submit_message()

	def Menu_Click(self, sender, e):
		sender.ContextMenu.IsOpen = True
	
	def Menu_Exit_Click(self, sender, e):
		self.send_message("/quit")
		self.Close()
	
	#CLIENT STUFF
	#submits message from text box
	def submit_message(self):
		self.handle_send_command(self.ui.myMessage.Text)
		self.ui.myMessage.Text = ''

	#sends message to server
	def send_message(self, message):
		self.client.send(message)

	def connect(self, params):
		self.client = Client()
		self.client.connect(host = '127.0.0.1')
		self.clientThread = threading.Thread(target=self.client_thread)
		self.clientThread.start()

	def handle_send_command(self, msg):
		params = msg.split(' ')
		op = params[0].lower()

		if op == '/connect' and not self.client.isClientConnected:
			self.connect(params)
		else:
			self.send_message(msg)

	def client_thread(self):
		while True:
			#get data from socket
			data = self.client.receive()
			commands = filter(None, data.split("\n"))

			#delimit by \n, otherwise multiple commands may come in one \n
			for command in commands:
				#handle commands from serv
				params = command.split(' ')
				op = params[0]
				if op == '/servername':
					self.recv_server_name(" ".join(params[1:]))
				#elif op == '/quit':
				#	self.client.disconnect()
				else:
					self.model.messages += command + "\n"
					self.isNewMessage = True

	#RECV HANDLERS
	def recv_server_name(self, name):
		self.model.serverName = name
