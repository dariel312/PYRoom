class ChannelOP():
	def __init__(self, operation, name):
		self.op = operation
		self.name = name
		self.message = ""

class ChannelVM():
	def __init__(self, name, listbox):
		self.name = name
		self.listbox = listbox
		self.messages = ''
		self.joined = False
		
class AppVM():
	def __init__(self):
		self.messages = ''
		self.myMessages = ''
		self.serverName = 'PyRoom'
		self.isNewMessage = False
		self.currentChannel = None
		self.channels = {}
		self.channelQueue = []
