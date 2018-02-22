import wpf
from System import TimeSpan
from System.Windows.Controls import *
from System.Windows import *
from System.Windows.Threading import *
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

		#setup ui threadupdate
		self.updater = DispatcherTimer()
		self.updater.Tick += self.update_UI
		self.updater.Interval = TimeSpan(0,0,0,0,33)
		self.updater.Start()

		self.client = Client()
	
    #updates ui for data changes
	def update_UI(self, sender, e):
		self.ui.messages.Text = self.model.messages

	#GUI STUFF
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
		self.handle_command(self.ui.myMessage.Text)
		self.ui.myMessage.Text = ''

	#CLIENT STUFF
	def client_thread(self):
		while True:
			#get data from socket
		    data = self.client.receive()
		    self.model.messages += data

	def send_message(self, message):
	    self.client.send(message)

	def connect(self, params):
		self.client.connect(host = '127.0.0.1')
		self.clientThread = threading.Thread(target=self.client_thread)
		self.clientThread.start()

	def handle_command(self, msg):
		params = msg.split(' ')
		op = params[0].lower()

		if op == '/connect':
			self.connect(params)
		else:
			self.send_message(msg)