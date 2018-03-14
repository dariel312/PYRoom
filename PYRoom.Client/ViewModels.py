class ChannelQueue():
	def __init__(self, operation, name):
		self.op = operation
		self.name = name

class ChatRoomListItemVM():
    def __init__(self):
        self.name = "Johns Room"
        self.userCount = 10

class AppVM():
	def __init__(self):
		self.messages = ''
		self.myMessages = ''
		self.serverName = 'PyRoom'
		self.isNewMessage = False
		self.channelQueue = []
		self.userQueue = []