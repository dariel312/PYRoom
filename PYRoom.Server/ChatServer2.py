import socket
import sys
import threading
import Channel

class Server:
    SERVER_CONFIG = {"MAX_CONNECTIONS": 15}

    HELP_MESSAGE = """\n> The list of commands available are:

/help                   - Show the instructions
/join [channel_name]    - To create or switch to a channel.
/quit                   - Exits the program.
/list                   - Lists all available channels.\n\n""".encode('utf8')

    def __init__(self, host=socket.gethostbyname('localhost'), port=50000, allowReuseAddress=True):
        self.address = (host, port)
        self.channels = {} # Channel Name -> Channel
        self.channels_client_map = {} # Client Name -> Channel Name

        try:
            self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as errorMessage:
            sys.stderr.write("Failed to initialize the server. Error - %s\n", str(errorMessage))
            raise

        if allowReuseAddress:
            self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            self.serverSocket.bind(self.address)
        except socket.error as errorMessage:
            sys.stderr.write('Failed to bind to ' + self.address + '. Error - %s\n', str(errorMessage))
            raise

    def listen_thread(self, defaultGreeting="\n> Welcome to our chat app!!! What is your name?\n"):
        while True:
            print("Waiting for a client to establish a connection\n")
            clientSocket, clientAddress = self.serverSocket.accept()
            print("Connection established with IP address {0} and port {1}\n".format(clientAddress[0], clientAddress[1]))
            self.welcome_client(clientSocket)
            clientThread = threading.Thread(target=self.client_thread, args=(clientSocket,))
            clientThread.start()

    def start_listening(self):
        self.serverSocket.listen(Server.SERVER_CONFIG["MAX_CONNECTIONS"])
        listenerThread = threading.Thread(target=self.listen_thread)
        listenerThread.start()
        listenerThread.join()

    def welcome_client(self, clientSocket):
        clientSocket.sendall("\n> Welcome to our chat app!!! What is your name?\n".encode('utf8'))

    def client_thread(self, clientSocket, size=4096):
        clientName = clientSocket.recv(size).decode('utf8')
        welcomeMessage = '> Welcome %s, type /help for a list of helpful commands.\n\n' % clientName
        clientSocket.send(welcomeMessage.encode('utf8'))

        while True:
            chatMessage = clientSocket.recv(size).decode('utf8').lower()

            if not chatMessage:
                break

            if '/quit' in chatMessage:
                self.quit(clientSocket, clientName)
                break
            elif '/list' in chatMessage:
                self.list_all_channels(clientSocket)
            elif '/help' in chatMessage:
                self.help(clientSocket)
            elif '/join' in chatMessage:
                self.join(clientSocket, chatMessage, clientName)
            else:
                self.send_message(clientSocket, chatMessage + '\n' , clientName)

        clientSocket.close()

    def quit(self, clientSocket, clientName):
        clientSocket.sendall('/quit'.encode('utf8'))
        self.remove_client(clientName)

    def list_all_channels(self, clientSocket):
        if len(self.channels) == 0:
            chatMessage = "\n> No rooms available. Create your own by typing /join [channel_name]\n"
            clientSocket.sendall(chatMessage.encode('utf8'))
        else:
            chatMessage = '\n\n> Current channels available are: \n'
            for channel in self.channels:
                chatMessage += "    \n" + channel + ": " + str(len(self.channels[channel].clients)) + " user(s)"
            chatMessage += "\n"
            clientSocket.sendall(chatMessage.encode('utf8'))

    def help(self, clientSocket):
        clientSocket.sendall(Server.HELP_MESSAGE)

    def join(self, clientSocket, chatMessage, clientName):
        isInSameRoom = False

        if len(chatMessage.split()) >= 2:
            channelName = chatMessage.split()[1]

            if clientName in self.channels_client_map: # Here we are switching to a new channel.
                if self.channels_client_map[clientName] == channelName:
                    clientSocket.sendall(("\n> You are already in channel: " + channelName).encode('utf8'))
                    isInSameRoom = True
                else: # switch to a new channel
                    oldChannelName = self.channels_client_map[clientName]
                    self.channels[oldChannelName].remove_client_from_channel(clientName) # remove them from the previous channel

            if not isInSameRoom:
                if not channelName in self.channels:
                    newChannel = Channel.Channel(channelName)
                    self.channels[channelName] = newChannel

                self.channels[channelName].clients[clientName] = clientSocket
                self.channels[channelName].welcome_client(clientName)
                self.channels_client_map[clientName] = channelName
        else:
            self.help(clientSocket)

    def send_message(self, clientSocket, chatMessage, clientName):
        if clientName in self.channels_client_map:
            self.channels[self.channels_client_map[clientName]].broadcast_message(chatMessage, clientName + ": ")
        else:
            chatMessage = """\n> You are currently not in any channels:

Use /list to see a list of available channels.
Use /join [channel name] to join a channels.\n\n""".encode('utf8')

            clientSocket.sendall(chatMessage)

    def remove_client(self, clientName):
        if clientName in self.channels_client_map:
            self.channels[self.channels_client_map[clientName]].remove_client_from_channel(clientName)
            del self.channels_client_map[clientName]
        print("Client: " + clientName + " has left\n")

    def server_shutdown(self):
        print("Shutting down chat server.\n")
        self.serverSocket.shutdown(socket.SHUT_RDWR)
        self.serverSocket.close()

def main():
    chatServer = Server()

    print("\nListening on port " + str(chatServer.address[1]))
    print("Waiting for connections...\n")

    chatServer.start_listening()
    chatServer.server_shutdown()

if __name__ == "__main__":
    main()
