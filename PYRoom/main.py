import threading
import socket
import sys

def thread_receive(sock):
	#test send
	sock.sendall("Test sending data to socket!".encode())
	
	#test recv
	msg = sock.recv(4096)
	print(msg.decode())
	sock.close()
	
#main
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = ('localhost', 9000)
sock.bind(address)
sock.listen(16)

print("Accepting connections connections")
while True:
	#accept connections
	connection, client_addr = sock.accept()
	thrd = threading.Thread(target=thread_receive, args=(connection,))
	thrd.start()

