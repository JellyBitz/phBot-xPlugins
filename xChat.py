from phBot import *
import phBotChat
import QtBind

pVersion = 'v0.0.2'

# Avoid possible issues
inGame = False

# Globals
delayMsg = 10000 # delay between messages
delayCounter = 0

# Initializing GUI
gui = QtBind.init(__name__,"xChat")
cbxMsg = QtBind.createCheckBox(gui, 'cbxMsg_clicked','Send message: ', 21, 13)
cbxMsg_checked = False
tbxMsg = QtBind.createLineEdit(gui,"",130,12,590,18)
lblSpamCounter = QtBind.createLabel(gui,"Spam Counter:",21,35)
lblCounter = QtBind.createLabel(gui,"0",90,35)

# Check to start sending messages
def cbxMsg_clicked(checked):
	global cbxMsg_checked
	cbxMsg_checked = checked
	if checked:
		# restart spamer counter
		global delayCounter
		delayCounter = 0
		QtBind.setText(gui,lblCounter,"0")
		log("Plugin: Starting spam")
	else:
		log("Plugin: Stopping spam")

# Send message, even through script. Ex. "chat,All,Hello World!" or "chat,private,JellyBitz,Hi!"
def chat(args):
	# check arguments length and empty message
	if (len(args) >= 3 and len(args[2]) > 0):
		success = False
		type = args[1].lower()
		if type == "all":
			success = phBotChat.All(args[2])
		elif type == "private":
			success = phBotChat.Private(args[2],args[3])
		elif type == "party":
			success = phBotChat.Party(args[2])
		elif type == "guild":
			success = phBotChat.Guild(args[2])
		elif type == "union":
			success = phBotChat.Union(args[2])
		elif type == "note":
			success = phBotChat.Note(args[2],args[3])
		elif type == "stall":
			success = phBotChat.Stall(args[2])
		if success:
			log("Plugin: Message sent successfully (xChat)")

# Called when the bot successfully connects to the game server
def connected():
	global inGame
	inGame = False

# Called when the character enters the game world
def joined_game():
	global inGame
	inGame = True

# Called every 500ms.
def event_loop():
	if inGame:
		if cbxMsg_checked:
			global delayCounter
			delayCounter += 500
			if delayCounter%delayMsg == 0:
				chat(['chat','All',QtBind.text(gui,tbxMsg)])
				QtBind.setText(gui,lblCounter,str(int(QtBind.text(gui,lblCounter))+1))

# Plugin load success
log('Plugin: xChat '+pVersion+' successfully loaded.')