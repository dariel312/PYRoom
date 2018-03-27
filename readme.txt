Dariel's Chat room. 
Written By: Dariel Barroso
PID: 5679436

I certify that this is my own work.


Video Link:



***********************************
SERVER:
***********************************
Server is located in a seperate folder\project called PYRoom.Server
The server was written using sample 2 with channels given to us, but I had to make a lot of changes to make it run for me.

To Run:
> py PYRoom.Server/main.py

WORKING CHAT COMMANDS
/connect <host> <port>  - Connects your ChatRoom Client to the server (Handled in the client)
/help                   - Show the instructions
/nick <new name>		- Changes your display name if the name is not registered
/join <channel name>    - To create or switch to a channel.
/part <channel name>	- Leaves a channel
/quit                   - Exits the program.
/info					- Displays info about the server
/list                   - Lists all available channels.
/version				- Displays the server version
/ping <message>			- Server replies with PONG <message>
/away <message>			- Sets yourself as away, private messages will elicit an automatic reply with <message>. Message is optional
/privmsg <user> <message> - Sends a direct message to the specified user.
/notice  <user> <message> - Same as privmsg but does not return an automatic reply from away users.
/users					- Returns a list of users connected to the server
/userhost <users>		-Returns the host for the specified users
/userip <users>			-Returns the IP of the specified users.
/rules					-Returns list of rules
/time					-Returns the local timestamp of the server
/whois <users>			-Returns detailed information about the user
/kick <user> <channel>	-Kicks a user from a channel, must be an operator.
/die					-Shuts down the server, must be an operator.
/silence <users>		-Silences specified users, must be an operator.
/setname <name>			-Sets your real name. Spaces allowed
/topic <channel> <topic> - Sets the topic of the channel. If topic is ommited, then will return the topic if the channel.

COMMAND LINE INTERACTION
/die
/usercount
/users
/channels
/restart

COMMAND LINE ARGS:
-p <listener port>
-db <db path> 



***********************************
CLIENT:
***********************************

The client was written from scratch using Windows Presentation Foundation (WPF).
For it to run you must have IronPython installed otherwise it will not work.

Download: http://ironpython.net/download/


To Run (Iron Python command):
> ipy PyRoom.Client/main.py

COMMAND LINE Args:
-host <host ip>
-p <host port>
-t <test file>

Some Interesting things about the client:
-There is no file menu (Too old and basic)
-There is a button in the dropdown menu on the right of the screen that allows you to clear the chat window
-There is a button between the Channel list and the chat window that allows you to collapse the channel list panel
-Upon connecting to the server the title of the window and the Header above the chat window will update to the name of the chat server
-The whole design of the GUI was written XAML (similar to XML and HTML)
-Supports multichannel


***********************************
WHATS MISSING
***********************************
-Commands
	/kill
	/knock
	/mode
	/user
	/wallops
	/who

-No log files
-No configuration files