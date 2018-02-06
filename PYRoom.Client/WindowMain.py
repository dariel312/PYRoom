import wpf
from NewChatRoomPrompt import *
from System.Windows import *

class WindowMain(Window):

    def __init__(self):
        self.ui = wpf.LoadComponent(self, 'WindowMain.xaml')
        self.sidebar = self.ui.sidebar

    def SideBar_ToggleClick(self, sender, e):
        if (self.sidebar.Visibility == Visibility.Collapsed):
            self.sidebar.Visibility = Visibility.Visible
        else:
            self.sidebar.Visibility = Visibility.Collapsed
    
    def NewRoom_Click(self, sender, e):
      MessageBox.Show("Click new roomn")
      
             


    