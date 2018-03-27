

class Const:
	WELCOME_INITIAL = "> Welcome to our Dariel's Chat Server!!!"
	WELCOME_MESSAGE = '> Welcome %s, type /help for a list of helpful commands.'
	LIST_ALL_USERS = '> The users in the chat room are: '
	LIST_ALL_CHANNELS = '> The channels in this room are are: '
	NOT_CHANNEL_MESSAGE = "> You are currently not in any channels:\n> Use /list to see a list of available channels.\n> Use /join [channel name] to join a channels."
	ALREADY_IN_CHANNEL =  "> You are already in channel: " 
	SERVER_VERSION = "> Server Version: {0}"
	DISCONNECTED = "> You have been disconnected."
	NO_CHANNELS = "> There are currently no channels created."
	CHANNEL_USER_COUNT = "> There are currently {0} users in this channel."
	INFO = "> This is my Server, made by Dariel Barroso."
	USER_TAKEN = "> This name is already registered. Please use a different nickname or log in using command /USER <username> <password>"
	CHANGED_NAME = "> {0} has changed nickname to {1}"
	MSG_USER_NOT_FOUND = "> {0} can not be found on this server."
	IS_ON = "> Is On: {0}"
	MUST_BE_OP = "> Must be an operator to perform this command."
	SHUTTING_DOWN = "> Server is shutting down."
	USERS =  "> Nick: {0}\tChannel: {2}"
	SETNAME_SUCCESS = "> Real name changed to {0}."
	WHO_IS = "> Nick: {0}\tReal: {1}\tAway: {2}\tAuthenticated: {3}\tChannel(s): {4}"
	HELP_MESSAGE = """
> The list of commands available are:
/help                   - Show the instructions
/connect <host> <port>  - Connects your ChatRoom Client to the server (Handled in the client)
/nick <new name>		- Changes your display name if the name is not registered
/join <channle name>   - To create or switch to a channel.
/part <channel name>	- Leaves a channel
/quit                   - Exits the program.
/info					- Displays info about the server
/list                   - Lists all available channels.
/version				- Displays the server version
/ping <message>			- Server replies with PONG <message>
/away <message>			- Sets yourself as away, private messages will elicit an automatic reply with <message>. Message is optional
/pass <password>		- Sends password in an attempt to register connected. /pass must be proceded with /user
/user <username> <hostname> <servername> <realname> -Logs you in as a to a registered user.
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
"""
	
	RULES = """
> These are the Server Rules:
1. No Cursing, If a MOD catches you cursing, it is an automatic ban.
2. No impersonating, do not impersonate other users.
3. Label links with NSFW (Not safe for work) when link includes innapropriate content such as nudity, violence, blood and gore
"""