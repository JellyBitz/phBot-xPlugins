from phBot import *
import QtBind
import urllib.request
import urllib.parse
import struct
import json
import os

pName = 'JellyDix'
pVersion = '0.0.1'
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

lblTriggers = QtBind.createLabel(gui,"Check all notifications that you wish on Discord :",6,45)
cbxEvtSpawn_uniqueNear = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Unique spawns near',6, 64)
cbxEvtSpawn_uniqueSpawn = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Unique spawn',6, 83)
cbxEvtSpawn_uniqueKilled = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Unique killed',6, 102)

cbxEvtDrop_item = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Item drop',6,121)
cbxEvtDrop_rare = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Rare drop',6,140)

cbxEvtSpawn_hunter = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Hunter/Trader spawn',6,159)
cbxEvtSpawn_thief = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Thief spawn',6,178)
cbxEvtChar_attacked = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Character attacked',6,197)
cbxEvtChar_died = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Character died',6,216)
cbxEvtPet_transport_died = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Transport/Horse died',6,235)

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
			if "cbxEvtSpawn_hunter" in triggers and triggers["cbxEvtSpawn_hunter"]:
				QtBind.setChecked(gui,cbxEvtSpawn_hunter,True)
			if "cbxEvtSpawn_thief" in triggers and triggers["cbxEvtSpawn_thief"]:
				QtBind.setChecked(gui,cbxEvtSpawn_thief,True)
			if "cbxEvtChar_attacked" in triggers and triggers["cbxEvtChar_attacked"]:
				QtBind.setChecked(gui,cbxEvtChar_attacked,True)
			if "cbxEvtChar_died" in triggers and triggers["cbxEvtChar_died"]:
				QtBind.setChecked(gui,cbxEvtChar_died,True)
			if "cbxEvtPet_transport_died" in triggers and triggers["cbxEvtPet_transport_died"]:
				QtBind.setChecked(gui,cbxEvtPet_transport_died,True)
			if "cbxEvtDrop_item" in triggers and triggers["cbxEvtDrop_item"]:
				QtBind.setChecked(gui,cbxEvtDrop_item,True)
			if "cbxEvtDrop_rare" in triggers and triggers["cbxEvtDrop_rare"]:
				QtBind.setChecked(gui,cbxEvtDrop_rare,True)

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
		triggers["cbxEvtSpawn_hunter"] = QtBind.isChecked(gui,cbxEvtSpawn_hunter)
		triggers["cbxEvtSpawn_thief"] = QtBind.isChecked(gui,cbxEvtSpawn_thief)
		triggers["cbxEvtChar_attacked"] = QtBind.isChecked(gui,cbxEvtChar_attacked)
		triggers["cbxEvtChar_died"] = QtBind.isChecked(gui,cbxEvtChar_died)
		triggers["cbxEvtPet_transport_died"] = QtBind.isChecked(gui,cbxEvtPet_transport_died)
		triggers["cbxEvtDrop_item"] = QtBind.isChecked(gui,cbxEvtDrop_item)
		triggers["cbxEvtDrop_rare"] = QtBind.isChecked(gui,cbxEvtDrop_rare)
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
		jsonData = {"key":key,"channel":channelID,"message":"**"+character_data['name']+"**: "+message}
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
	if t == 0 and QtBind.isChecked(gui,cbxEvtSpawn_uniqueNear):
		SendNotification("["+data+"] unique spawn near to you!")
	elif t == 1 and QtBind.isChecked(gui,cbxEvtSpawn_hunter):
		SendNotification("[Hunter or Trader] spawn near to you!")
	elif t == 2 and QtBind.isChecked(gui,cbxEvtSpawn_thief):
		SendNotification("[Thief] spawn near to you!")
	elif t == 3 and QtBind.isChecked(gui,cbxEvtPet_transport_died):
		t = get_pets()[data]
		SendNotification("Your pet ["+(t['type'].title())+" died")
	elif t == 4 and QtBind.isChecked(gui,cbxEvtChar_attacked):
		SendNotification("["+data+"] is attacking you!")
	elif t == 5 and QtBind.isChecked(gui,cbxEvtDrop_rare):
		t = get_item(int(data))
		SendNotification("You picked up a [Rare] item ["+t['name']+"]")
	elif t == 6 and QtBind.isChecked(gui,cbxEvtDrop_item):
		t = get_item(int(data))
		SendNotification("You picked up an item ["+t['name']+"]")
	elif t == 7 and QtBind.isChecked(gui,cbxEvtChar_died):
		SendNotification("You died :(")

# All packets received from Silkroad will be passed to this function
# Returning True will keep the packet and False will not forward it to the game server
def handle_joymax(opcode, data):
	if opcode == 0x300C:
		updateType = data[0]
		if updateType == 5:
			if QtBind.isChecked(gui,cbxEvtSpawn_uniqueSpawn):
				modelID = struct.unpack_from("<I",data,2)[0]
				unique = get_monster(int(uniqueModelID))
				SendNotification("["+unique['name']+"] spawned")
		elif updateType == 6:
			if QtBind.isChecked(gui,cbxEvtSpawn_uniqueSpawn):
				modelID = struct.unpack_from("<I",data,2)[0]
				killerNameLength = struct.unpack_from('<H', data, 6)[0]
				killerName = struct.unpack_from('<' + str(charLength) + 's', data, 8)[0].decode('cp1252')
				unique = get_monster(int(uniqueModelID))
				SendNotification("["+unique['name']+"] killed by ["+killerName+"]")
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