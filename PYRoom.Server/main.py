from ChatServer import ChatServer

def main():
    chatServer = ChatServer()
    print("\nListening on port " + str(chatServer.port))
    print("Waiting for connections...\n")

    chatServer.start_listening()
    chatServer.server_shutdown()

if __name__ == "__main__":
    main()
