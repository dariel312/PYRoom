import wpf

from System.Windows import Window

class NewChatRoomPrompt(Window):
    def __init__(self):
        wpf.LoadComponent(self, 'NewChatRoomPrompt.xaml')


