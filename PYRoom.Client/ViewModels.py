
class ChatRoomVM():
    def __init__(self):
        self.name = "Johns Room"
        self.messages = ""
        self.myMessage = ""

class ChatRoomListItemVM():
    def __init__(self):
        self.name = "Johns Room"
        self.userCount = 10
        self.roomID = 0

class AppVM():
    def __init__(self):
        self.messages = ''
        self.myMessages = ''
        self.chatRoomList = [ChatRoomListItemVM(), ChatRoomListItemVM(), ChatRoomListItemVM(), ChatRoomListItemVM(), ChatRoomListItemVM()]
