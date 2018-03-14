

class Const:
	WELCOME_INITIAL = "> Welcome to our Dariel's Chat Server!!!"
	WELCOME_MESSAGE = '> Welcome %s, type /help for a list of helpful commands.'
	LIST_ALL_USERS = '> The users in the chat room are: '
	LIST_ALL_CHANNELS = '> The channels in this room are room are: '
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
	HELP_MESSAGE = """
> The list of commands available are:
/help                   - Show the instructions
/nick <new name>		- Changes your display name if the name is not registered
/join [channel_name]    - To create or switch to a channel.
/quit                   - Exits the program.
/info					- Displays info about the server
/list                   - Lists all available channels.
/version				- Displays the server version
/ping <message>			- Server replies with PONG <message>
/away <message>			- Sets yourself as away, private messages will elicit an automatic reply with <message>. Message is optional
/pass <password>		- Sends password in an attempt to register connected. /pass must be proceded with /user
/user <username> <hostname> <servername> <realname> -Logs you in as a to a registered user.
/privmsg <user> <message> - Sends a direct message to the specified user."""
	
