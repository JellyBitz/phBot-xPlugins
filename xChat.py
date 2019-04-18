from phBot import *
from time import localtime, strftime
import phBotChat
import QtBind
import json
import os

pName = 'xChat'
pVersion = '0.2.0'

# Avoid issues
inGame = False

# Globals
delayMsg = 10000 # delay between messages
delayCounter = 0
character_data = None

# Initializing GUI
gui = QtBind.init(__name__,pName)
cbxMsg = QtBind.createCheckBox(gui, 'cbxMsg_clicked','Send message: ', 21, 13)
cbxMsg_checked = False
tbxMsg = QtBind.createLineEdit(gui,"",125,12,480,18)
lblSpamCounter = QtBind.createLabel(gui,"Spam Counter :",620,13)
lblCounter = QtBind.createLabel(gui,"0",700,13)

lblLog = QtBind.createLabel(gui,"Now you can log all ingame messages! Just select the type of chat messages that you want to log.",21,45)
cbxLogAll = QtBind.createCheckBox(gui,'cbxLog_clicked','All', 21, 64)
cbxLogPrivate = QtBind.createCheckBox(gui,'cbxLog_clicked','Private', 21, 83)
cbxLogParty = QtBind.createCheckBox(gui,'cbxLog_clicked','Party', 21, 102)
cbxLogGuild = QtBind.createCheckBox(gui,'cbxLog_clicked','Guild', 21, 121)
cbxLogUnion = QtBind.createCheckBox(gui,'cbxLog_clicked','Union', 21, 140)
cbxLogAcademy = QtBind.createCheckBox(gui,'cbxLog_clicked','Academy', 21, 159)
cbxLogStall = QtBind.createCheckBox(gui,'cbxLog_clicked','Stall', 21, 178)
cbxLogGlobal = QtBind.createCheckBox(gui,'cbxLog_clicked','Global', 21, 197)
cbxLogNotice = QtBind.createCheckBox(gui,'cbxLog_clicked','Notice', 21, 216)
cbxLogGM = QtBind.createCheckBox(gui,'cbxLog_clicked','GM', 21, 235)
cbxLogUnknown = QtBind.createCheckBox(gui,'cbxLog_clicked','All Others', 21, 254)

cbxLogsInOne = QtBind.createCheckBox(gui, 'cbxLog_clicked','Save messages in one file (log.txt)', 500, 45)

# Return folder path
def getPath():
	return get_config_dir()+pName+"\\"

# Return character configs path (JSON)
def getConfig():
	return getPath()+character_data["server"]+"_"+character_data["name"]+".json"

# Load default configs
def loadDefaultConfig():
	# Clear data
	QtBind.setChecked(gui,cbxLogAll,False)
	QtBind.setChecked(gui,cbxLogPrivate,False)
	QtBind.setChecked(gui,cbxLogParty,False)
	QtBind.setChecked(gui,cbxLogGuild,False)
	QtBind.setChecked(gui,cbxLogUnion,False)
	QtBind.setChecked(gui,cbxLogStall,False)
	QtBind.setChecked(gui,cbxLogGlobal,False)
	QtBind.setChecked(gui,cbxLogNotice,False)
	QtBind.setChecked(gui,cbxLogGM,False)
	QtBind.setChecked(gui,cbxLogUnknown,False)

# Load config if exists
def loadConfig():
	loadDefaultConfig()
	if os.path.exists(getConfig()):
		data = {}
		with open(getConfig(),"r") as f:
			data = json.load(f)
		# Check to load config
		if "cbxLogAll" in data and data["cbxLogAll"]:
			QtBind.setChecked(gui,cbxLogAll,data["cbxLogAll"])
		if "cbxLogPrivate" in data and data["cbxLogPrivate"]:
			QtBind.setChecked(gui,cbxLogPrivate,data["cbxLogPrivate"])
		if "cbxLogParty" in data and data["cbxLogParty"]:
			QtBind.setChecked(gui,cbxLogParty,data["cbxLogParty"])
		if "cbxLogGuild" in data and data["cbxLogGuild"]:
			QtBind.setChecked(gui,cbxLogGuild,data["cbxLogGuild"])
		if "cbxLogUnion" in data and data["cbxLogUnion"]:
			QtBind.setChecked(gui,cbxLogUnion,data["cbxLogUnion"])
		if "cbxLogAcademy" in data and data["cbxLogAcademy"]:
			QtBind.setChecked(gui,cbxLogAcademy,data["cbxLogAcademy"])
		if "cbxLogStall" in data and data["cbxLogStall"]:
			QtBind.setChecked(gui,cbxLogStall,data["cbxLogStall"])
		if "cbxLogGlobal" in data and data["cbxLogGlobal"]:
			QtBind.setChecked(gui,cbxLogGlobal,data["cbxLogGlobal"])
		if "cbxLogNotice" in data and data["cbxLogNotice"]:
			QtBind.setChecked(gui,cbxLogNotice,data["cbxLogNotice"])
		if "cbxLogGM" in data and data["cbxLogGM"]:
			QtBind.setChecked(gui,cbxLogGM,data["cbxLogGM"])
		if "cbxLogUnknown" in data and data["cbxLogUnknown"]:
			QtBind.setChecked(gui,cbxLogUnknown,data["cbxLogUnknown"])
		if "cbxLogsInOne" in data and data["cbxLogsInOne"]:
			QtBind.setChecked(gui,cbxLogsInOne,data["cbxLogsInOne"])

# Save specific value at config
def saveConfig(key,value):
	if key:
		data = {}
		if os.path.exists(getConfig()):
			with open(getConfig(),"r") as f:
				data = json.load(f)
		data[key] = value
		with open(getConfig(),"w") as f:
			f.write(json.dumps(data, indent=4, sort_keys=True))

# Called when the bot successfully connects to the game server
def connected():
	global inGame
	inGame = False

# Called when the character enters the game world
def joined_game():
	global inGame,character_data
	inGame = True
	character_data = get_character_data()
	loadConfig()

# Just saving everything everytime (slower method)
def cbxLog_clicked():
	saveConfig("cbxLogAll",QtBind.isChecked(gui,cbxLogAll))
	saveConfig("cbxLogPrivate",QtBind.isChecked(gui,cbxLogPrivate))
	saveConfig("cbxLogParty",QtBind.isChecked(gui,cbxLogParty))
	saveConfig("cbxLogGuild",QtBind.isChecked(gui,cbxLogGuild))
	saveConfig("cbxLogUnion",QtBind.isChecked(gui,cbxLogUnion))
	saveConfig("cbxLogAcademy",QtBind.isChecked(gui,cbxLogAcademy))
	saveConfig("cbxLogStall",QtBind.isChecked(gui,cbxLogStall))
	saveConfig("cbxLogGlobal",QtBind.isChecked(gui,cbxLogGlobal))
	saveConfig("cbxLogNotice",QtBind.isChecked(gui,cbxLogNotice))
	saveConfig("cbxLogGM",QtBind.isChecked(gui,cbxLogGM))
	saveConfig("cbxLogUnknown",QtBind.isChecked(gui,cbxLogUnknown))
	saveConfig("cbxLogsInOne",QtBind.isChecked(gui,cbxLogsInOne))

# All chat messages received are sent to this function
def handle_chat(t,player,msg):
	p = player
	if not p:
		p = ""
	# Check message type
	if t == 1 and QtBind.isChecked(gui,cbxLogAll):
		logline(["","[All]"+p+":"+msg])
	elif t == 2 and QtBind.isChecked(gui,cbxLogPrivate):
		logline(["","[Private]"+p+":"+msg])
	elif t == 3 and QtBind.isChecked(gui,cbxLogGM):
		logline(["","[GM]"+p+":"+msg])
	elif t == 4 and QtBind.isChecked(gui,cbxLogParty):
		logline(["","[Party]"+p+":"+msg])
	elif t == 5 and QtBind.isChecked(gui,cbxLogGuild):
		logline(["","[Guild]"+p+":"+msg])
	elif t == 6 and QtBind.isChecked(gui,cbxLogGlobal):
		logline(["","[Global]"+p+":"+msg])
	elif t == 7 and QtBind.isChecked(gui,cbxLogNotice):
		logline(["","[Notice]"+p+":"+msg])
	elif t == 9 and QtBind.isChecked(gui,cbxLogStall):
		logline(["","[Stall]"+p+":"+msg])
	elif t == 11 and QtBind.isChecked(gui,cbxLogUnion):
		logline(["","[Union]"+p+":"+msg])
	elif t == 16 and QtBind.isChecked(gui,cbxLogAcademy):
		logline(["","[Academy]"+p+":"+msg])
	elif QtBind.isChecked(gui,cbxLogUnknown):
		logline(["","[Other("+str(t)+")]"+p+":"+msg])

# Save message to the log.txt "logline,text"
def logline(args):
	if len(args) == 2:
		path = "log.txt" if QtBind.isChecked(gui,cbxLogsInOne) else character_data["server"]+"_"+character_data["name"]+"_log.txt"
		date = strftime("%d/%m %I:%M:%S %p", localtime())
		with open(getPath()+path,"a+") as f:
			f.write(date+" > "+args[1])

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
			log("Plugin: Message sent successfully ("+pName+")")

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
log('Plugin: '+pName+' v'+pVersion+' successfully loaded.')
# Creating configs folder
if not os.path.exists(getPath()):
	os.makedirs(getPath())
	log('Plugin: '+pName+' folder has been created.')
# Check if module exists
try:
	import xPluginUpdater
	xPluginUpdater.Check(pVersion,'https://raw.githubusercontent.com/JellyBitz/phBot-xPlugins/master/'+pName+'.py')
except:
	pass