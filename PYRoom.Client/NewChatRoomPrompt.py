import wpf
from System.Windows.Controls import *
from System.Windows import *
from NewChatRoomPrompt import *
from ViewModels import *
from System.Windows import Window

class NewChatRoomPrompt(Window):
    def __init__(self):
        self.ui = wpf.LoadComponent(self, 'NewChatRoomPrompt.xaml')
        self.name = ''
        self.result = False

    def getName(self):
        return self.name
    
    def Click_Submit(self, sender, e):
        self.name = self.ui.input_name
        self.result = True
   
     


