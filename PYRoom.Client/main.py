import wpf
from System.Windows import Application, Window
from WindowMain import WindowMain
import sys
import argparse


if __name__ == '__main__':

	#parser = argparse.ArgumentParser()
	#parser.add_argument("-p", "--p", type=int, help="Port number to connect to by default")
	#parser.add_argument("-h", "--host", type=str, help="Host IP to connect to by default")

	#args = parser.parse_args()

	Application().Run(WindowMain())

	 