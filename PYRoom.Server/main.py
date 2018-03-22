from ChatServer import ChatServer

import argparse

def main():
	global isRestart
	isRestart = True

	#get args
	parser = argparse.ArgumentParser()
	parser.add_argument("-p", "--p", type=int, help="Port number to listen connect to by default")
	parser.add_argument("-db", "--db", type=str, help="Directory of stored db files.")
	args = parser.parse_args()


	while isRestart:
		isRestart = False
		chatServer = ChatServer(port=args.p, dbPath = args.db)
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
