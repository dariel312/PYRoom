import wpf
from System.Windows.Controls import *
from System.Windows import *
from ViewModels import *
from System.Windows import Window

class ConnectPrompt(Window):
	def __init__(self):
		self.ui = wpf.LoadComponent(self, 'ConnectPrompt.xaml')
		self.host = ''
		self.port = 0
		self.result = False

	def getName(self):
		return self.name
	
	def Click_Submit(self, sender, e):
		self.host = self.ui.input_host.Text
		self.port = self.ui.input_port.Text
		self.result = True
