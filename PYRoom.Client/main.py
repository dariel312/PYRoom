import wpf
from System.Windows import Application, Window
from WindowMain import WindowMain
import sys
import argparse


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-p", "--p", type=int, help="Port number to connect to by default")
	parser.add_argument("-host", "--host", type=str, help="Host IP to connect to by default")
	parser.add_argument("-t", "--test", type=str, help="File to read and run test form")
	args = parser.parse_args()

	Application().Run(WindowMain(host = args.host, port=args.p, testFile = args.test))

	 