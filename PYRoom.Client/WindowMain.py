import wpf
from System.Windows.Controls import *
from System.Windows import *
from NewChatRoomPrompt import *
from ViewModels import *

class WindowMain(Window):

	def __init__(self):
		self.ui = wpf.LoadComponent(self, 'WindowMain.xaml')
		self.sidebar = self.ui.sidebar
		self.DataContext = AppVM()	#holds all the data to be displayed
		

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
			MessageBox.Show("You canceled this new room.");