from phBot import *
import QtBind
import urllib.request
import urllib.parse
import struct
import json
import os

pName = 'JellyDix'
pVersion = '0.0.5'
pUrl = 'https://raw.githubusercontent.com/JellyBitz/phBot-xPlugins/master/JellyDix.py'

# Globals
character_data = None

# Default data
JELLYDIX_KEY="JellyDix"
JELLYDIX_URL="https://JellyDix.jellybitz.repl.co"

# Initializing GUI
gui = QtBind.init(__name__,pName)
lblKey = QtBind.createLabel(gui,"JellyDix Key :",6,10)
tbxKey = QtBind.createLineEdit(gui,"",75,7,80,18)
lblChannel = QtBind.createLabel(gui,"Discord Channel :",170,10)
tbxChannel = QtBind.createLineEdit(gui,"",258,7,120,18)
lblUrl = QtBind.createLabel(gui,"Website Url :",400,10)
tbxUrl = QtBind.createLineEdit(gui,"",466,7,180,18)
btnSaveConfig = QtBind.createButton(gui,'saveConfigs',"  Save  ",660,7)

# uniques
lblTriggers = QtBind.createLabel(gui,"Check all notifications that you wish on Discord :",6,45)
cbxEvtSpawn_uniqueNear = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Unique spawns near',6, 64)
cbxEvtSpawn_uniqueSpawn = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Unique spawn',6, 83)
cbxEvtSpawn_uniqueKilled = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Unique killed',6, 102)

# picks
cbxEvtDrop_item = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Item drop',6,121)
cbxEvtDrop_rare = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Rare drop',6,140)

# warnings
cbxEvtNear_hunter = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Hunter/Trader spawn',6,159)
cbxEvtNear_thief = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Thief spawn',6,178)
cbxEvtChar_attacked = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Character attacked',6,197)
cbxEvtChar_died = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Character died',6,216)
cbxEvtPet_died = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Transport/Horse died',6,235)

# messages
cbxEvtMessage_private = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Private',156, 64)
cbxEvtMessage_party = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Party',156, 83)
cbxEvtMessage_academy = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Academy',156, 102)
cbxEvtMessage_guild = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Guild',156, 121)
cbxEvtMessage_stall = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Stall',156, 140)
cbxEvtMessage_global = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Global',156, 159)
cbxEvtMessage_notice = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Notice',156, 178)
cbxEvtMessage_gm = QtBind.createCheckBox(gui,'cbxTrigger_clicked','GM',156, 198)
cbxEvtMessage_battlearena = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Battle Arena',156, 216)
cbxEvtMessage_ctf = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Capture the Flag',156, 235)
cbxEvtMessage_quest = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Quest completed',156, 254)

# Return folder path
def getPath():
	return get_config_dir()+pName+"\\"

# Return character configs path (JSON)
def getConfig():
	return getPath()+character_data['server'] + "_" + character_data['name'] + ".json"

# Load default configs
def loadDefaultConfig():
	# Clear data
	QtBind.setText(gui, tbxKey,JELLYDIX_KEY)
	QtBind.setText(gui, tbxChannel,"")
	QtBind.setText(gui, tbxUrl,JELLYDIX_URL)
	# Triggers
	QtBind.setChecked(gui,cbxEvtSpawn_uniqueNear,False)
	QtBind.setChecked(gui,cbxEvtSpawn_uniqueSpawn,False)
	QtBind.setChecked(gui,cbxEvtSpawn_uniqueKilled,False)
	QtBind.setChecked(gui,cbxEvtNear_hunter,False)
	QtBind.setChecked(gui,cbxEvtNear_thief,False)
	QtBind.setChecked(gui,cbxEvtChar_attacked,False)
	QtBind.setChecked(gui,cbxEvtChar_died,False)
	QtBind.setChecked(gui,cbxEvtPet_died,False)
	QtBind.setChecked(gui,cbxEvtDrop_item,False)
	QtBind.setChecked(gui,cbxEvtDrop_rare,False)
	QtBind.setChecked(gui,cbxEvtMessage_private,False)
	QtBind.setChecked(gui,cbxEvtMessage_party,False)
	QtBind.setChecked(gui,cbxEvtMessage_academy,False)
	QtBind.setChecked(gui,cbxEvtMessage_guild,False)
	QtBind.setChecked(gui,cbxEvtMessage_stall,False)
	QtBind.setChecked(gui,cbxEvtMessage_global,False)
	QtBind.setChecked(gui,cbxEvtMessage_notice,False)
	QtBind.setChecked(gui,cbxEvtMessage_gm,False)
	QtBind.setChecked(gui,cbxEvtMessage_battlearena,False)
	QtBind.setChecked(gui,cbxEvtMessage_ctf,False)
	QtBind.setChecked(gui,cbxEvtMessage_quest,False)

# Loads all config previously saved
def loadConfigs():
	loadDefaultConfig()
	# Check config exists to load
	if os.path.exists(getConfig()):
		data = {}
		with open(getConfig(),"r") as f:
			data = json.load(f)
		# Load all data
		if "Key" in data:
			QtBind.setText(gui, tbxKey,data["Key"])
		if "Channel" in data:
			QtBind.setText(gui, tbxChannel,data["Channel"])
		if "Url" in data:
			QtBind.setText(gui, tbxUrl,data["Url"])
		# Load triggers
		if "Triggers" in data:
			triggers = data["Triggers"]
			if "cbxEvtSpawn_uniqueNear" in triggers and triggers["cbxEvtSpawn_uniqueNear"]:
				QtBind.setChecked(gui,cbxEvtSpawn_uniqueNear,True)
			if "cbxEvtSpawn_uniqueSpawn" in triggers and triggers["cbxEvtSpawn_uniqueSpawn"]:
				QtBind.setChecked(gui,cbxEvtSpawn_uniqueSpawn,True)
			if "cbxEvtSpawn_uniqueKilled" in triggers and triggers["cbxEvtSpawn_uniqueKilled"]:
				QtBind.setChecked(gui,cbxEvtSpawn_uniqueKilled,True)
			if "cbxEvtNear_hunter" in triggers and triggers["cbxEvtNear_hunter"]:
				QtBind.setChecked(gui,cbxEvtNear_hunter,True)
			if "cbxEvtNear_thief" in triggers and triggers["cbxEvtNear_thief"]:
				QtBind.setChecked(gui,cbxEvtNear_thief,True)
			if "cbxEvtChar_attacked" in triggers and triggers["cbxEvtChar_attacked"]:
				QtBind.setChecked(gui,cbxEvtChar_attacked,True)
			if "cbxEvtChar_died" in triggers and triggers["cbxEvtChar_died"]:
				QtBind.setChecked(gui,cbxEvtChar_died,True)
			if "cbxEvtPet_died" in triggers and triggers["cbxEvtPet_died"]:
				QtBind.setChecked(gui,cbxEvtPet_died,True)
			if "cbxEvtDrop_item" in triggers and triggers["cbxEvtDrop_item"]:
				QtBind.setChecked(gui,cbxEvtDrop_item,True)
			if "cbxEvtDrop_rare" in triggers and triggers["cbxEvtDrop_rare"]:
				QtBind.setChecked(gui,cbxEvtDrop_rare,True)
			if "cbxEvtMessage_private" in triggers and triggers["cbxEvtMessage_private"]:
				QtBind.setChecked(gui,cbxEvtMessage_private,True)
			if "cbxEvtMessage_party" in triggers and triggers["cbxEvtMessage_party"]:
				QtBind.setChecked(gui,cbxEvtMessage_party,True)
			if "cbxEvtMessage_academy" in triggers and triggers["cbxEvtMessage_academy"]:
				QtBind.setChecked(gui,cbxEvtMessage_academy,True)
			if "cbxEvtMessage_guild" in triggers and triggers["cbxEvtMessage_guild"]:
				QtBind.setChecked(gui,cbxEvtMessage_guild,True)
			if "cbxEvtMessage_stall" in triggers and triggers["cbxEvtMessage_stall"]:
				QtBind.setChecked(gui,cbxEvtMessage_stall,True)
			if "cbxEvtMessage_global" in triggers and triggers["cbxEvtMessage_global"]:
				QtBind.setChecked(gui,cbxEvtMessage_global,True)
			if "cbxEvtMessage_notice" in triggers and triggers["cbxEvtMessage_notice"]:
				QtBind.setChecked(gui,cbxEvtMessage_notice,True)
			if "cbxEvtMessage_gm" in triggers and triggers["cbxEvtMessage_gm"]:
				QtBind.setChecked(gui,cbxEvtMessage_gm,True)
			if "cbxEvtMessage_battlearena" in triggers and triggers["cbxEvtMessage_battlearena"]:
				QtBind.setChecked(gui,cbxEvtMessage_battlearena,True)
			if "cbxEvtMessage_ctf" in triggers and triggers["cbxEvtMessage_ctf"]:
				QtBind.setChecked(gui,cbxEvtMessage_ctf,True)
			if "cbxEvtMessage_quest" in triggers and triggers["cbxEvtMessage_quest"]:
				QtBind.setChecked(gui,cbxEvtMessage_quest,True)

# Save specific value at config
def saveConfigs():
	# Save if data has been loaded
	if character_data:
		# Save all data
		data = {}
		data["Key"] = QtBind.text(gui,tbxKey)
		data["Channel"] = QtBind.text(gui,tbxChannel)
		data["Url"] = QtBind.text(gui,tbxUrl)
		# Save triggers
		triggers = {}
		data["Triggers"] = triggers
		triggers["cbxEvtSpawn_uniqueNear"] = QtBind.isChecked(gui,cbxEvtSpawn_uniqueNear)
		triggers["cbxEvtSpawn_uniqueSpawn"] = QtBind.isChecked(gui,cbxEvtSpawn_uniqueSpawn)
		triggers["cbxEvtSpawn_uniqueKilled"] = QtBind.isChecked(gui,cbxEvtSpawn_uniqueKilled)
		triggers["cbxEvtNear_hunter"] = QtBind.isChecked(gui,cbxEvtNear_hunter)
		triggers["cbxEvtNear_thief"] = QtBind.isChecked(gui,cbxEvtNear_thief)
		triggers["cbxEvtChar_attacked"] = QtBind.isChecked(gui,cbxEvtChar_attacked)
		triggers["cbxEvtChar_died"] = QtBind.isChecked(gui,cbxEvtChar_died)
		triggers["cbxEvtPet_died"] = QtBind.isChecked(gui,cbxEvtPet_died)
		triggers["cbxEvtDrop_item"] = QtBind.isChecked(gui,cbxEvtDrop_item)
		triggers["cbxEvtDrop_rare"] = QtBind.isChecked(gui,cbxEvtDrop_rare)
		triggers["cbxEvtMessage_private"] = QtBind.isChecked(gui,cbxEvtMessage_private)
		triggers["cbxEvtMessage_party"] = QtBind.isChecked(gui,cbxEvtMessage_party)
		triggers["cbxEvtMessage_academy"] = QtBind.isChecked(gui,cbxEvtMessage_academy)
		triggers["cbxEvtMessage_guild"] = QtBind.isChecked(gui,cbxEvtMessage_guild)
		triggers["cbxEvtMessage_stall"] = QtBind.isChecked(gui,cbxEvtMessage_stall)
		triggers["cbxEvtMessage_global"] = QtBind.isChecked(gui,cbxEvtMessage_global)
		triggers["cbxEvtMessage_notice"] = QtBind.isChecked(gui,cbxEvtMessage_notice)
		triggers["cbxEvtMessage_gm"] = QtBind.isChecked(gui,cbxEvtMessage_gm)
		triggers["cbxEvtMessage_battlearena"] = QtBind.isChecked(gui,cbxEvtMessage_battlearena)
		triggers["cbxEvtMessage_ctf"] = QtBind.isChecked(gui,cbxEvtMessage_ctf)
		triggers["cbxEvtMessage_quest"] = QtBind.isChecked(gui,cbxEvtMessage_quest)
		# Overrides
		with open(getConfig(),"w") as f:
			f.write(json.dumps(data, indent=4, sort_keys=True))

# Checkbox trigger clicked
def cbxTrigger_clicked(checked):
	saveConfigs()

# Called when the character enters the game world
def joined_game():
	global character_data
	character_data = get_character_data()
	loadConfigs()

# Send message to discord
def SendNotification(message,channelID=None):
	# Load channel from GUI
	if not channelID:
		channelID = QtBind.text(gui,tbxChannel)
	# Check if there is enough data
	key = QtBind.text(gui,tbxKey)
	if not key or not channelID or not message:
		return
	# Try to send notification
	try:
		# Prepare json to send through POST method
		jsonData = {"key":key,"channel":channelID,"message":message}
		# Setup
		params = json.dumps(jsonData).encode('utf8')
		url = QtBind.text(gui,tbxUrl)
		if not url.endswith("/"):
			url += "/"
		req = urllib.request.Request(url+"api",data=params,headers={'content-type': 'application/json'})
		with urllib.request.urlopen(req,timeout=5) as f:
			try:
				success = f.read().decode('utf-8')
				if success == 'true':
					log("Plugin: Notification sent to Discord")
				else:
					log("Plugin: Notification failed loading..")
			except Exception as ex:
				log("Plugin: Error reading response from server ["+str(ex)+"]")
	except Exception as e:
		log("Plugin: Error loading url ["+str(e)+"]")

# Called for specific events. data field will always be a string.
def handle_event(t, data):
	# Filter events
	msgHeader = "**"+character_data['name']+"** - "
	if t == 0 and QtBind.isChecked(gui,cbxEvtSpawn_uniqueNear):
		SendNotification(msgHeader+"["+data+"] unique spawn near to you!")
	elif t == 1 and QtBind.isChecked(gui,cbxEvtNear_hunter):
		SendNotification(msgHeader+"Hunter or Trader ["+data+"] spawn near to you!")
	elif t == 2 and QtBind.isChecked(gui,cbxEvtNear_thief):
		SendNotification(msgHeader+"Thief ["+data+"] spawn near to you!")
	elif t == 3 and QtBind.isChecked(gui,cbxEvtPet_died):
		t = get_pets()[data]
		SendNotification(msgHeader+"Pet ["+(t['type'].title())+" died")
	elif t == 4 and QtBind.isChecked(gui,cbxEvtChar_attacked):
		SendNotification(msgHeader+"["+data+"] is attacking you!")
	elif t == 5 and QtBind.isChecked(gui,cbxEvtDrop_rare):
		t = get_item(int(data))
		SendNotification(msgHeader+"Item (Rare) picked up ["+t['name']+"]")
	elif t == 6 and QtBind.isChecked(gui,cbxEvtDrop_item):
		t = get_item(int(data))
		SendNotification(msgHeader+"Item picked up ["+t['name']+"]")
	elif t == 7 and QtBind.isChecked(gui,cbxEvtChar_died):
		SendNotification(msgHeader+"You died")

# All chat messages received are sent to this function
def handle_chat(t,player,msg):
	msgHeader = "**"+character_data['name']+"** - "
	# Check message type
	if t == 2 and QtBind.isChecked(gui,cbxEvtMessage_private):
		SendNotification(msgHeader+"**[Private] from ["+player+"]: "+msg)
	elif t == 3 and QtBind.isChecked(gui,cbxEvtMessage_gm):
		SendNotification("[GM] **"+player+"** : "+msg)
	elif t == 4 and QtBind.isChecked(gui,cbxEvtMessage_party):
		SendNotification("[Party] **"+player+"** : "+msg)
	elif t == 5 and QtBind.isChecked(gui,cbxEvtMessage_guild):
		SendNotification("[Guild] **"+player+"** : "+msg)
	elif t == 6 and QtBind.isChecked(gui,cbxEvtMessage_global):
		SendNotification("[Global] **"+player+"** : "+msg)
	elif t == 7 and QtBind.isChecked(gui,cbxEvtMessage_notice):
		SendNotification("[Notice] "+msg)
	elif t == 9 and QtBind.isChecked(gui,cbxEvtMessage_stall):
		SendNotification(msgHeader+"[Stall] from ["+player+"] : "+msg)
	elif t == 16 and QtBind.isChecked(gui,cbxEvtMessage_academy):
		SendNotification("[Academy] **"+player+"** : "+msg)

# All packets received from Silkroad will be passed to this function
# Returning True will keep the packet and False will not forward it to the game server
def handle_joymax(opcode, data):
	if opcode == 0x300C:
		updateType = data[0]
		if updateType == 5:
			if QtBind.isChecked(gui,cbxEvtSpawn_uniqueSpawn):
				modelID = struct.unpack_from("<I",data,2)[0]
				unique = get_monster(int(modelID))
				SendNotification("["+unique['name']+"] spawned")
		elif updateType == 6:
			if QtBind.isChecked(gui,cbxEvtSpawn_uniqueKilled):
				modelID = struct.unpack_from("<I",data,2)[0]
				killerNameLength = struct.unpack_from('<H', data, 6)[0]
				killerName = struct.unpack_from('<' + str(killerNameLength) + 's', data, 8)[0].decode('cp1252')
				unique = get_monster(int(modelID))
				SendNotification("["+unique['name']+"] killed by ["+killerName+"]")
	elif opcode == 0x34D2:
		if QtBind.isChecked(gui,cbxEvtMessage_battlearena):
			updateType = data[0]
			if updateType == 2:
				SendNotification("[Battle Arena] starts at 15 min.")
			elif updateType == 13:
				SendNotification("[Battle Arena] starts at 5 min.")
			elif updateType == 14:
				SendNotification("[Battle Arena] starts at 1 min.")
			elif updateType == 3:
				SendNotification("[Battle Arena] registration closed")
			elif updateType == 4:
				SendNotification("[Battle Arena] started")
			elif updateType == 5:
				SendNotification("[Battle Arena] finished")
	elif opcode == 0x34B1:
		if QtBind.isChecked(gui,cbxEvtMessage_ctf):
			updateType = data[0]
			if updateType == 2:
				SendNotification("[Capture the Flag] starts at 15 min.")
			elif updateType == 13:
				SendNotification("[Capture the Flag] starts at 5 min.")
			elif updateType == 14:
				SendNotification("[Capture the Flag] starts at 1 min.")
			elif updateType == 3:
				SendNotification("[Capture the Flag] started")
			elif updateType == 9:
				SendNotification("[Capture the Flag] finished")
	elif opcode == 0x30D5:
		if QtBind.isChecked(gui,cbxEvtMessage_quest):
			# Quest updated & Quest completed
			if data[0] == 2 and data[10] == 2:
				strLength = struct.unpack_from('<H', data, 11)[0]
				questServerName = struct.unpack_from('<' + str(strLength) + 's', data, 13)[0].decode('cp1252')
				SendNotification("**"+character_data['name']+"** - [Quest] has been completed ["+questServerName+"]")
	return True

# Plugin load success
log('Plugin: '+pName+' v'+pVersion+' successfully loaded')

# Creating configs folder
if os.path.exists(getPath()):
	# Adding RELOAD plugin support
	character_data = get_character_data()
	if character_data:
		loadConfigs()
else:
	os.makedirs(getPath())
	log('Plugin: '+pName+' folder has been created')