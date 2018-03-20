from System.Windows import Application, Window
from WindowMain import WindowMain
import sys
import argparse


if __name__ == '__main__':
	if len(sys.argv) > 0:
		for x in range(0, len(sys.argv)):
			if argv[x]  == '-h':
				host = argv[x+1]
			elif argv[x] == '-p':
				port = argv[x+1]

	Application().Run(WindowMain())

	 