from ChatServer import ChatServer


def main():
	global isRestart
	isRestart = True

	while isRestart:
		isRestart = False
		chatServer = ChatServer()
		print("\nListening on port " + str(chatServer.port))
		print("Waiting for connections...\n")
		chatServer.start_listening()

		#server commands
		while True:
			line = input()

			if line == '/die':
				chatServer.server_shutdown()
				break;
			elif line == '/userscount':
				print(len(chatServer.clients) + " Users currently online")
			elif line == '/users':
				for client in chatServer.clients.values():
					print(client.name, client.socket.getsockname())
			elif line == '/channels':
				for channel in chatServer.channels.values():
					print(channel.name)
			elif line == '/restart':
				chatServer.server_shutdown()
				isRestart = True
				break
			else:
				print("Unknown command. Commands are /die, /usercount, /users, /channels, /restart")

if __name__ == "__main__":
	main()
