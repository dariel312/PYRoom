import wpf
from System.Windows import Application, Window
from WindowMain import WindowMain
import socket
import sys

## Create a TCP/IP socket
#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

## Connect the socket to the port where the server is listening
#server_address = ('localhost', 9000)
#print('connecting to %s port %s' % server_address)
#sock.connect(server_address)
#msg = sock.recv(4096)
#print(msg.decode())
#print('test')

if __name__ == '__main__':
    Application().Run(WindowMain())

