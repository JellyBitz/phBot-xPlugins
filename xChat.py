from phBot import *
from time import localtime, strftime
import phBotChat
import QtBind
import json
import os

pName = 'xChat'
pVersion = '1.2.1'
pUrl = 'https://raw.githubusercontent.com/JellyBitz/phBot-xPlugins/master/xChat.py'

# ______________________________ Initializing ______________________________ #

# Globals
MESSAGES_DELAY = 10000 # delay between messages (ms)
message_delay_counter = 0
character_data = None

# Graphic user interface
gui = QtBind.init(__name__,pName)
cbxMsg = QtBind.createCheckBox(gui, 'cbxMsg_clicked','Send message: ', 21, 13)
cbxMsg_checked = False
tbxMsg = QtBind.createLineEdit(gui,"",125,12,480,18)
lblSpamCounter = QtBind.createLabel(gui,"Spam Counter :",620,13)
lblCounter = QtBind.createLabel(gui,"0",700,13)

lblLog = QtBind.createLabel(gui,"Now you can log all ingame messages! Just select the type of chat messages that you want to log.",21,45)
cbxLogsInOne = QtBind.createCheckBox(gui, 'cbxLog_clicked','Save messages in one file (log.txt)', 500, 45)

cbxLogAll = QtBind.createCheckBox(gui,'cbxLog_clicked','All',21,64)
cbxLogPrivate = QtBind.createCheckBox(gui,'cbxLog_clicked','Private',21,83)
cbxLogParty = QtBind.createCheckBox(gui,'cbxLog_clicked','Party',21,102)
cbxLogGuild = QtBind.createCheckBox(gui,'cbxLog_clicked','Guild',21,121)
cbxLogUnion = QtBind.createCheckBox(gui,'cbxLog_clicked','Union',21,140)
cbxLogAcademy = QtBind.createCheckBox(gui,'cbxLog_clicked','Academy',21,159)
cbxLogStall = QtBind.createCheckBox(gui,'cbxLog_clicked','Stall',21,178)
cbxLogGlobal = QtBind.createCheckBox(gui,'cbxLog_clicked','Global',21,197)
cbxLogNotice = QtBind.createCheckBox(gui,'cbxLog_clicked','Notice',21,216)
cbxLogGM = QtBind.createCheckBox(gui,'cbxLog_clicked','GM',21,235)
cbxLogUnknown = QtBind.createCheckBox(gui,'cbxLog_clicked','All Others',21, 254)

cbxEvtSpawn_unique = QtBind.createCheckBox(gui,'cbxLog_clicked','Unique spawn',321, 64)
cbxEvtSpawn_hunter = QtBind.createCheckBox(gui,'cbxLog_clicked','Hunter/Trader spawn',321,83)
cbxEvtSpawn_thief = QtBind.createCheckBox(gui,'cbxLog_clicked','Thief spawn',321,102)
cbxEvtChar_attacked = QtBind.createCheckBox(gui,'cbxLog_clicked','Character attacked',321,121)
cbxEvtChar_died = QtBind.createCheckBox(gui,'cbxLog_clicked','Character died',321,140)
cbxEvtPet_transport_died = QtBind.createCheckBox(gui,'cbxLog_clicked','Transport/Horse died',321,159)
cbxEvtDrop_item = QtBind.createCheckBox(gui,'cbxLog_clicked','Item drop',321,178)
cbxEvtDrop_rare = QtBind.createCheckBox(gui,'cbxLog_clicked','Rare drop',321,197)

# ______________________________ Methods ______________________________ #

# Return folder path
def getPath():
	return get_config_dir()+pName+"\\"

# Return character configs path (JSON)
def getConfig():
	return getPath()+character_data["server"]+"_"+character_data["name"]+".json"

# Load default configs
def loadDefaultConfig():
	# Clear data
	QtBind.setChecked(gui,cbxLogsInOne,False)
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
	QtBind.setChecked(gui,cbxEvtSpawn_unique,False)
	QtBind.setChecked(gui,cbxEvtSpawn_hunter,False)
	QtBind.setChecked(gui,cbxEvtSpawn_thief,False)
	QtBind.setChecked(gui,cbxEvtChar_attacked,False)
	QtBind.setChecked(gui,cbxEvtChar_died,False)
	QtBind.setChecked(gui,cbxEvtPet_transport_died,False)
	QtBind.setChecked(gui,cbxEvtDrop_item,False)
	QtBind.setChecked(gui,cbxEvtDrop_rare,False)

# Loads all config previously saved
def loadConfigs():
	loadDefaultConfig()
	if isJoined():

		if os.path.exists(getConfig()):
			data = {}
			with open(getConfig(),"r") as f:
				data = json.load(f)

			# Check to load config
			if "cbxLogsInOne" in data and data["cbxLogsInOne"]:
				QtBind.setChecked(gui,cbxLogsInOne,data["cbxLogsInOne"])
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
			if "cbxEvtSpawn_unique" in data and data["cbxEvtSpawn_unique"]:
				QtBind.setChecked(gui,cbxEvtSpawn_unique,data["cbxEvtSpawn_unique"])
			if "cbxEvtSpawn_hunter" in data and data["cbxEvtSpawn_hunter"]:
				QtBind.setChecked(gui,cbxEvtSpawn_hunter,data["cbxEvtSpawn_hunter"])
			if "cbxEvtSpawn_thief" in data and data["cbxEvtSpawn_thief"]:
				QtBind.setChecked(gui,cbxEvtSpawn_thief,data["cbxEvtSpawn_thief"])
			if "cbxEvtChar_attacked" in data and data["cbxEvtChar_attacked"]:
				QtBind.setChecked(gui,cbxEvtChar_attacked,data["cbxEvtChar_attacked"])
			if "cbxEvtChar_died" in data and data["cbxEvtChar_died"]:
				QtBind.setChecked(gui,cbxEvtChar_died,data["cbxEvtChar_died"])
			if "cbxEvtPet_transport_died" in data and data["cbxEvtPet_transport_died"]:
				QtBind.setChecked(gui,cbxEvtPet_transport_died,data["cbxEvtPet_transport_died"])
			if "cbxEvtDrop_item" in data and data["cbxEvtDrop_item"]:
				QtBind.setChecked(gui,cbxEvtDrop_item,data["cbxEvtDrop_item"])
			if "cbxEvtDrop_rare" in data and data["cbxEvtDrop_rare"]:
				QtBind.setChecked(gui,cbxEvtDrop_rare,data["cbxEvtDrop_rare"])

# Save all config
def saveConfigs():
	# Save if data has been loaded
	if isJoined():
		# Save all data
		data = {}
		data["cbxLogsInOne"] = QtBind.isChecked(gui,cbxLogsInOne)
		data["cbxLogAll"] = QtBind.isChecked(gui,cbxLogAll)
		data["cbxLogPrivate"] = QtBind.isChecked(gui,cbxLogPrivate)
		data["cbxLogParty"] = QtBind.isChecked(gui,cbxLogParty)
		data["cbxLogGuild"] = QtBind.isChecked(gui,cbxLogGuild)
		data["cbxLogUnion"] = QtBind.isChecked(gui,cbxLogUnion)
		data["cbxLogAcademy"] = QtBind.isChecked(gui,cbxLogAcademy)
		data["cbxLogStall"] = QtBind.isChecked(gui,cbxLogStall)
		data["cbxLogGlobal"] = QtBind.isChecked(gui,cbxLogGlobal)
		data["cbxLogNotice"] = QtBind.isChecked(gui,cbxLogNotice)
		data["cbxLogGM"] = QtBind.isChecked(gui,cbxLogGM)
		data["cbxLogUnknown"] = QtBind.isChecked(gui,cbxLogUnknown)
		data["cbxEvtSpawn_unique"] = QtBind.isChecked(gui,cbxEvtSpawn_unique)
		data["cbxEvtSpawn_hunter"] = QtBind.isChecked(gui,cbxEvtSpawn_hunter)
		data["cbxEvtSpawn_thief"] = QtBind.isChecked(gui,cbxEvtSpawn_thief)
		data["cbxEvtChar_attacked"] = QtBind.isChecked(gui,cbxEvtChar_attacked)
		data["cbxEvtChar_died"] = QtBind.isChecked(gui,cbxEvtChar_died)
		data["cbxEvtPet_transport_died"] = QtBind.isChecked(gui,cbxEvtPet_transport_died)
		data["cbxEvtDrop_item"] = QtBind.isChecked(gui,cbxEvtDrop_item)
		data["cbxEvtDrop_rare"] = QtBind.isChecked(gui,cbxEvtDrop_rare)

		# Overrides
		with open(getConfig(),"w") as f:
			f.write(json.dumps(data, indent=4, sort_keys=True))
		log("Plugin: "+pName+" configs has been saved")

# Check if character is ingame
def isJoined():
	global character_data
	character_data = get_character_data()
	return character_data and "name" in character_data and character_data["name"]

# Just saving everything everytime (slower method)
def cbxLog_clicked(checked):
	saveConfigs()

# Check to start sending messages
def cbxMsg_clicked(checked):
	global cbxMsg_checked
	cbxMsg_checked = checked
	if checked:
		# restart spamer counter
		global message_delay_counter
		message_delay_counter = 0
		QtBind.setText(gui,lblCounter,"0")
		log("Plugin: Starting spam")
	else:
		log("Plugin: Stopping spam")

# Fix array comma handled by bot
def FixEscapeComma(_array):
	_len = len(_array)
	i = 0
	while i < _len:
		# Check if any argument ends with '\'
		if _array[i].endswith('\\') and i < (_len-1):
			_array[i] = _array[i][:-1]+','+_array[i+1]
			del _array[i+1]
			_len-=1
		else:
			i+=1
	return _array
# ______________________________ Events ______________________________ #

# Send message, even through script. Ex. "chat,All,Hello World!" or "chat,private,JellyBitz,Hi!"
def chat(args):
	args = FixEscapeComma(args)
	# Avoid wrong structure and empty stuffs
	if len(args) < 3 or not args[1] or not args[2]:
		return
	# Check message type
	sent = False
	t = args[1].lower()
	if t == "all":
		sent = phBotChat.All(args[2])
	elif t == "private":
		sent = phBotChat.Private(args[2],args[3])
	elif t == "party":
		sent = phBotChat.Party(args[2])
	elif t == "guild":
		sent = phBotChat.Guild(args[2])
	elif t == "union":
		sent = phBotChat.Union(args[2])
	elif t == "note":
		sent = phBotChat.Note(args[2],args[3])
	elif t == "stall":
		sent = phBotChat.Stall(args[2])
	elif t == "global":
		sent = phBotChat.Global(args[2])
	if sent:
		log('Plugin: Message "'+t+'" sent successfully!')

# Save message to the log.txt "logline,text"
def logline(args):
	if len(args) == 2:
		path = "log.txt" if QtBind.isChecked(gui,cbxLogsInOne) else character_data["server"]+"_"+character_data["name"]+"_log.txt"
		date = strftime("%d/%m %I:%M:%S %p", localtime())
		with open(getPath()+path, "a", encoding='utf-8') as f:
			f.write(date+" > "+ (args[1]).encode('utf-8').decode('utf-8') +'\n')

# Called when the bot successfully connects to the game server
def connected():
	global character_data
	character_data = None

# Called when the character enters the game world
def joined_game():
	loadConfig()

# All chat messages received are sent to this function
def handle_chat(t,p,msg):
	# check if is discord message
	if t == 100:
		on_discord_command(msg)
		return

	# Logline stuffs
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

# Called for specific events. data field will always be a string.
def handle_event(t, data):
	if t == 0 and QtBind.isChecked(gui,cbxEvtSpawn_unique):
		logline(["","[Spawn][Unique]:"+data])
	elif t == 1 and QtBind.isChecked(gui,cbxEvtSpawn_hunter):
		logline(["","[Spawn][Hunter/Trader]:"+data])
	elif t == 2 and QtBind.isChecked(gui,cbxEvtSpawn_thief):
		logline(["","[Spawn][Thief]:"+data])
	elif t == 3 and QtBind.isChecked(gui,cbxEvtPet_transport_died):
		t = get_pets()[data]
		logline(["","[Pet]["+(t['type'].title())+"]:Died"])
	elif t == 4 and QtBind.isChecked(gui,cbxEvtChar_attacked):
		logline(["","[Character][Attacked]:"+data])
	elif t == 5 and QtBind.isChecked(gui,cbxEvtDrop_rare):
		t = get_item(int(data))
		logline(["","[Drop][Rare]:"+t['name']])
	elif t == 6 and QtBind.isChecked(gui,cbxEvtDrop_item):
		t = get_item(int(data))
		logline(["","[Drop]:"+t['name']])
	elif t == 7 and QtBind.isChecked(gui,cbxEvtChar_died):
		logline(["","[Character][Died]"])

# Called everytime a discord message 
def on_discord_command(cmd):
	# Try to split message
	args = cmd.split(' ',2)
	# Check if is a CHAT command
	if args[0].lower().startswith('chat'):
		# Check if the format is correct and is not empty
		if len(args) == 3 and args[1] and args[2]:
			# Split correctly for handle it as script
			t = args[1].lower()
			if t == 'private' or t == 'note':
				# then check message is not empty
				argsExtra = args[2].split(' ',1)
				if argsExtra[0] and argsExtra[1]:
					args.pop(2)
					chat(args+argsExtra)
			else:
				chat(args)

# Called every 500ms
def event_loop():
	if character_data:
		if cbxMsg_checked:
			global message_delay_counter
			message_delay_counter += 500
			if message_delay_counter >= MESSAGES_DELAY:
				message_delay_counter = 0
				message = QtBind.text(gui,tbxMsg)
				if message:
					phBotChat.All(QtBind.text(gui,tbxMsg))
					QtBind.setText(gui,lblCounter,str(int(QtBind.text(gui,lblCounter))+1))

# Plugin loaded
log('Plugin: '+pName+' v'+pVersion+' successfully loaded')

if os.path.exists(getPath()):
	# Adding RELOAD plugin support
	loadConfigs()
else:
	# Creating configs folder
	os.makedirs(getPath())
	log('Plugin: '+pName+' folder has been created')
