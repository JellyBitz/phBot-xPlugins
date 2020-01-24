from phBot import *
from datetime import datetime
import QtBind
import urllib.request
import urllib.parse
import struct
import json
import os
import re

pName = 'JellyDix'
pVersion = '0.1.2'
pUrl = 'https://raw.githubusercontent.com/JellyBitz/phBot-xPlugins/master/JellyDix.py'

# Globals
character_data = None

# Default data
JELLYDIX_KEY="JellyDix"
JELLYDIX_URL="https://jellydix.jellybitz.repl.co"

# Initializing GUI
gui = QtBind.init(__name__,pName)
lblKey = QtBind.createLabel(gui,"Public Key :",6,10)
tbxKey = QtBind.createLineEdit(gui,"",65,7,60,18)
lblChannel = QtBind.createLabel(gui,"Discord Channel :",140,10)
tbxChannel = QtBind.createLineEdit(gui,"",228,7,160,18)
lblUrl = QtBind.createLabel(gui,"Website/Host :",400,10)
tbxUrl = QtBind.createLineEdit(gui,"",476,7,160,18)
btnSaveConfig = QtBind.createButton(gui,'saveConfigs',"  Save  ",660,7)

lblTriggers = QtBind.createLabel(gui,"Check the notifications you wish to see on your Discord Channel -",6,35)
cbxAddTimeStamp = QtBind.createCheckBox(gui,'cbxTrigger_clicked',"Add TimeStamps",325,35)
lblInfoRegex = QtBind.createLabel(gui,"-  Note: All text filters are using regex!",428,35)

cbxEvtChar_joined = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Joined to Game',6,54)
# messages
cbxEvtMessage_private = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Private',6,74)
cbxEvtMessage_stall = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Stall',6,89)
cbxEvtMessage_party = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Party',6,104)
cbxEvtMessage_academy = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Academy',6,119)
cbxEvtMessage_guild = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Guild',6,134)
cbxEvtMessage_union = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Union',6,149)
cbxEvtMessage_gm = QtBind.createCheckBox(gui,'cbxTrigger_clicked','GameMaster',6,164)
cbxEvtMessage_notice = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Notice',6,179)
cbxEvtMessage_global = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Global',6,194)
cbxEvtMessage_global_filter = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Filtered messages',10,209)
tbxEvtMessage_global_filter = QtBind.createLineEdit(gui,"Filter messages",28,209,90,14)

# uniques
cbxEvtMessage_uniqueSpawn = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Unique spawn',6,229)
cbxEvtMessage_uniqueSpawn_filter = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Filtered name',10,244)
tbxEvtMessage_uniqueSpawn_filter = QtBind.createLineEdit(gui,"Filter name",28,244,90,14)
cbxEvtMessage_uniqueKilled = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Unique killed',6,259)

# warnings
cbxEvtNear_unique = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Unique near to you',140, 54)
cbxEvtNear_hunter = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Hunter/Trader near',140,69)
cbxEvtNear_thief = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Thief near',140,84)
cbxEvtChar_attacked = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Character attacked',140,99)
cbxEvtChar_died = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Character died',140,114)
cbxEvtPet_died = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Transport/Horse died',140,129)

# picks
cbxEvtDrop_item = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Any item picked up',140,149)
cbxEvtDrop_rare = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Rare item picked up',140,164)
cbxEvtDrop_equip = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Equipable item picked up',140,179)
cbxEvtDrop_filter = QtBind.createCheckBox(gui,'cbxTrigger_clicked','[ - - - - - - - - - - ]  picked up',140,194)
tbxEvtDrop_filter = QtBind.createLineEdit(gui,"Filter item name",158,194,85,14)

# events
cbxEvtMessage_battlearena = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Battle Arena',140,214)
cbxEvtMessage_ctf = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Capture the Flag',140,229)

# character
cbxEvtMessage_quest = QtBind.createCheckBox(gui,'cbxTrigger_clicked','Quest completed',140,249)

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
	QtBind.setChecked(gui,cbxAddTimeStamp,False)
	# Triggers
	QtBind.setChecked(gui,cbxEvtChar_joined,False)
	QtBind.setChecked(gui,cbxEvtMessage_private,False)
	QtBind.setChecked(gui,cbxEvtMessage_stall,False)
	QtBind.setChecked(gui,cbxEvtMessage_party,False)
	QtBind.setChecked(gui,cbxEvtMessage_academy,False)
	QtBind.setChecked(gui,cbxEvtMessage_guild,False)
	QtBind.setChecked(gui,cbxEvtMessage_union,False)
	QtBind.setChecked(gui,cbxEvtMessage_gm,False)
	QtBind.setChecked(gui,cbxEvtMessage_notice,False)
	QtBind.setChecked(gui,cbxEvtMessage_global,False)
	QtBind.setChecked(gui,cbxEvtMessage_global_filter,False)
	QtBind.setText(gui,tbxEvtMessage_global_filter,"Filter messages")
	QtBind.setChecked(gui,cbxEvtMessage_uniqueSpawn,False)
	QtBind.setChecked(gui,cbxEvtMessage_uniqueSpawn_filter,False)
	QtBind.setText(gui,tbxEvtMessage_uniqueSpawn_filter,"Filter name")
	QtBind.setChecked(gui,cbxEvtMessage_uniqueKilled,False)
	QtBind.setChecked(gui,cbxEvtNear_unique,False)
	QtBind.setChecked(gui,cbxEvtNear_hunter,False)
	QtBind.setChecked(gui,cbxEvtNear_thief,False)
	QtBind.setChecked(gui,cbxEvtChar_attacked,False)
	QtBind.setChecked(gui,cbxEvtChar_died,False)
	QtBind.setChecked(gui,cbxEvtPet_died,False)
	QtBind.setChecked(gui,cbxEvtDrop_item,False)
	QtBind.setChecked(gui,cbxEvtDrop_rare,False)
	QtBind.setChecked(gui,cbxEvtDrop_equip,False)
	QtBind.setChecked(gui,cbxEvtDrop_filter,False)
	QtBind.setText(gui,tbxEvtDrop_filter,"Filter item name")
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
		if "AddTimeStamp" in data and data["AddTimeStamp"]:
			QtBind.setChecked(gui,cbxAddTimeStamp,True)
		# Load triggers
		if "Triggers" in data:
			triggers = data["Triggers"]
			if "cbxEvtNear_unique" in triggers and triggers["cbxEvtNear_unique"]:
				QtBind.setChecked(gui,cbxEvtNear_unique,True)
			if "cbxEvtMessage_uniqueSpawn" in triggers and triggers["cbxEvtMessage_uniqueSpawn"]:
				QtBind.setChecked(gui,cbxEvtMessage_uniqueSpawn,True)
			if "cbxEvtMessage_uniqueSpawn_filter" in triggers and triggers["cbxEvtMessage_uniqueSpawn_filter"]:
				QtBind.setChecked(gui,cbxEvtMessage_uniqueSpawn_filter,True)
			if "tbxEvtMessage_uniqueSpawn_filter" in triggers:
				QtBind.setText(gui,tbxEvtMessage_uniqueSpawn_filter,triggers["tbxEvtMessage_uniqueSpawn_filter"])
			if "cbxEvtMessage_uniqueKilled" in triggers and triggers["cbxEvtMessage_uniqueKilled"]:
				QtBind.setChecked(gui,cbxEvtMessage_uniqueKilled,True)
			if "cbxEvtChar_joined" in triggers and triggers["cbxEvtChar_joined"]:
				QtBind.setChecked(gui,cbxEvtChar_joined,True)
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
			if "cbxEvtDrop_equip" in triggers and triggers["cbxEvtDrop_equip"]:
				QtBind.setChecked(gui,cbxEvtDrop_equip,True)
			if "cbxEvtDrop_filter" in triggers and triggers["cbxEvtDrop_filter"]:
				QtBind.setChecked(gui,cbxEvtDrop_filter,True)
			if "tbxEvtDrop_filter" in triggers:
				QtBind.setText(gui,tbxEvtDrop_filter,triggers["tbxEvtDrop_filter"])
			if "cbxEvtMessage_private" in triggers and triggers["cbxEvtMessage_private"]:
				QtBind.setChecked(gui,cbxEvtMessage_private,True)
			if "cbxEvtMessage_stall" in triggers and triggers["cbxEvtMessage_stall"]:
				QtBind.setChecked(gui,cbxEvtMessage_stall,True)
			if "cbxEvtMessage_party" in triggers and triggers["cbxEvtMessage_party"]:
				QtBind.setChecked(gui,cbxEvtMessage_party,True)
			if "cbxEvtMessage_academy" in triggers and triggers["cbxEvtMessage_academy"]:
				QtBind.setChecked(gui,cbxEvtMessage_academy,True)
			if "cbxEvtMessage_guild" in triggers and triggers["cbxEvtMessage_guild"]:
				QtBind.setChecked(gui,cbxEvtMessage_guild,True)
			if "cbxEvtMessage_union" in triggers and triggers["cbxEvtMessage_union"]:
				QtBind.setChecked(gui,cbxEvtMessage_union,True)
			if "cbxEvtMessage_global" in triggers and triggers["cbxEvtMessage_global"]:
				QtBind.setChecked(gui,cbxEvtMessage_global,True)
			if "cbxEvtMessage_global_filter" in triggers and triggers["cbxEvtMessage_global_filter"]:
				QtBind.setChecked(gui,cbxEvtMessage_global_filter,True)
			if "tbxEvtMessage_global_filter" in triggers:
				QtBind.setText(gui,tbxEvtMessage_global_filter,triggers["tbxEvtMessage_global_filter"])
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
		data["AddTimeStamp"] = QtBind.isChecked(gui,cbxAddTimeStamp)
		# Save triggers
		triggers = {}
		data["Triggers"] = triggers
		triggers["cbxEvtChar_joined"] = QtBind.isChecked(gui,cbxEvtChar_joined)
		triggers["cbxEvtMessage_private"] = QtBind.isChecked(gui,cbxEvtMessage_private)
		triggers["cbxEvtMessage_stall"] = QtBind.isChecked(gui,cbxEvtMessage_stall)
		triggers["cbxEvtMessage_party"] = QtBind.isChecked(gui,cbxEvtMessage_party)
		triggers["cbxEvtMessage_academy"] = QtBind.isChecked(gui,cbxEvtMessage_academy)
		triggers["cbxEvtMessage_guild"] = QtBind.isChecked(gui,cbxEvtMessage_guild)
		triggers["cbxEvtMessage_union"] = QtBind.isChecked(gui,cbxEvtMessage_union)
		triggers["cbxEvtMessage_gm"] = QtBind.isChecked(gui,cbxEvtMessage_gm)
		triggers["cbxEvtMessage_notice"] = QtBind.isChecked(gui,cbxEvtMessage_notice)
		triggers["cbxEvtMessage_global"] = QtBind.isChecked(gui,cbxEvtMessage_global)
		triggers["cbxEvtMessage_global_filter"] = QtBind.isChecked(gui,cbxEvtMessage_global_filter)
		triggers["tbxEvtMessage_global_filter"] = QtBind.text(gui,tbxEvtMessage_global_filter)
		triggers["cbxEvtMessage_uniqueSpawn"] = QtBind.isChecked(gui,cbxEvtMessage_uniqueSpawn)
		triggers["cbxEvtMessage_uniqueSpawn_filter"] = QtBind.isChecked(gui,cbxEvtMessage_uniqueSpawn_filter)
		triggers["tbxEvtMessage_uniqueSpawn_filter"] = QtBind.text(gui,tbxEvtMessage_uniqueSpawn_filter)
		triggers["cbxEvtMessage_uniqueKilled"] = QtBind.isChecked(gui,cbxEvtMessage_uniqueKilled)
		triggers["cbxEvtNear_unique"] = QtBind.isChecked(gui,cbxEvtNear_unique)
		triggers["cbxEvtNear_hunter"] = QtBind.isChecked(gui,cbxEvtNear_hunter)
		triggers["cbxEvtNear_thief"] = QtBind.isChecked(gui,cbxEvtNear_thief)
		triggers["cbxEvtChar_attacked"] = QtBind.isChecked(gui,cbxEvtChar_attacked)
		triggers["cbxEvtChar_died"] = QtBind.isChecked(gui,cbxEvtChar_died)
		triggers["cbxEvtPet_died"] = QtBind.isChecked(gui,cbxEvtPet_died)
		triggers["cbxEvtDrop_item"] = QtBind.isChecked(gui,cbxEvtDrop_item)
		triggers["cbxEvtDrop_rare"] = QtBind.isChecked(gui,cbxEvtDrop_rare)
		triggers["cbxEvtDrop_equip"] = QtBind.isChecked(gui,cbxEvtDrop_equip)
		triggers["cbxEvtDrop_filter"] = QtBind.isChecked(gui,cbxEvtDrop_filter)
		triggers["tbxEvtDrop_filter"] = QtBind.text(gui,tbxEvtDrop_filter)
		triggers["cbxEvtMessage_battlearena"] = QtBind.isChecked(gui,cbxEvtMessage_battlearena)
		triggers["cbxEvtMessage_ctf"] = QtBind.isChecked(gui,cbxEvtMessage_ctf)
		triggers["cbxEvtMessage_quest"] = QtBind.isChecked(gui,cbxEvtMessage_quest)
		# Overrides
		with open(getConfig(),"w") as f:
			f.write(json.dumps(data, indent=4, sort_keys=True))

# Checkbox trigger clicked
def cbxTrigger_clicked(checked):
	saveConfigs()

# Send a notify to discord
# message : Text shown as discord notify
# channel_id : ID from channel to be sent
# info : Extra data used at server for some notifications
def SendNotify(message,channel_id=None,info=None):
	# Load channel from GUI
	if not channel_id:
		channel_id = QtBind.text(gui,tbxChannel)
	# Check if there is enough data to create a notify
	key = QtBind.text(gui,tbxKey)
	url = QtBind.text(gui,tbxUrl)
	if not key or not channel_id or not message or not url:
		return
	# Try to send notify
	try:
		# Add timestamp
		if QtBind.isChecked(gui,cbxAddTimeStamp):
			message = "|`"+datetime.now().strftime('%H:%M:%S')+"`| "+message
		# Prepare json to send through POST method
		jsonData = {"key":key,"channel":channel_id,"message":message}
		if info:
			jsonData["info"] = info
		# Setup
		params = json.dumps(jsonData).encode('utf8')
		if not url.endswith("/"):
			url += "/"
		req = urllib.request.Request(url+"api",data=params,headers={'content-type': 'application/json'})
		with urllib.request.urlopen(req,timeout=5) as f:
			try:
				msg = f.read().decode('utf-8')
				if msg == 'true':
					log("Plugin: notify sent to Discord!")
				else:
					log("Plugin: notify failed ["+msg+"]")
			except Exception as ex2:
				log("Plugin: Error reading response from server ["+str(ex2)+"]")
	except Exception as ex:
		log("Plugin: Error loading url ["+str(ex)+"]")

# Called when the character enters the game world
def joined_game():
	global character_data
	character_data = get_character_data()
	loadConfigs()
	if QtBind.isChecked(gui,cbxEvtChar_joined):
		SendNotify("**"+character_data['name']+"** - Joined to the game")

# Called for specific events. data field will always be a string.
def handle_event(t, data):
	# Filter events
	msgHeader = "**"+character_data['name']+"** - "
	if t == 0 and QtBind.isChecked(gui,cbxEvtNear_unique):
		SendNotify(msgHeader+"["+data+"] unique is near to you!",info=CreateInfo("position",get_position()))
	elif t == 1 and QtBind.isChecked(gui,cbxEvtNear_hunter):
		SendNotify(msgHeader+"Hunter or Trader ["+data+"] is near to you!",info=CreateInfo("position",get_position()))
	elif t == 2 and QtBind.isChecked(gui,cbxEvtNear_thief):
		SendNotify(msgHeader+"Thief ["+data+"] is near to you!",info=CreateInfo("position",get_position()))
	elif t == 3 and QtBind.isChecked(gui,cbxEvtPet_died):
		t = get_pets()[data]
		SendNotify(msgHeader+"Pet ["+(t['type'].title())+"] died")
	elif t == 4 and QtBind.isChecked(gui,cbxEvtChar_attacked):
		SendNotify(msgHeader+"["+data+"] is attacking you!")
	elif t == 7 and QtBind.isChecked(gui,cbxEvtChar_died):
		SendNotify(msgHeader+"You died",info=CreateInfo("position",get_position()))

# All chat messages received are sent to this function
def handle_chat(t,player,msg):
	# Check message type
	if t == 2 and QtBind.isChecked(gui,cbxEvtMessage_private):
		SendNotify("**"+character_data['name']+"** - "+"[Private] from ["+player+"] : "+msg)
	elif t == 9 and QtBind.isChecked(gui,cbxEvtMessage_stall):
		SendNotify("**"+character_data['name']+"** - "+"[Stall] from ["+player+"] : "+msg)
	elif t == 4 and QtBind.isChecked(gui,cbxEvtMessage_party):
		SendNotify("**"+character_data['name']+"** - "+"[Party] **"+player+"** : "+msg)
	elif t == 16 and QtBind.isChecked(gui,cbxEvtMessage_academy):
		SendNotify("**"+character_data['name']+"** - "+"[Academy] **"+player+"** : "+msg)
	elif t == 5 and QtBind.isChecked(gui,cbxEvtMessage_guild):
		SendNotify("[Guild] **"+player+"** : "+msg)
	elif t == 11 and QtBind.isChecked(gui,cbxEvtMessage_union):
		SendNotify("[Union] **"+player+"** : "+msg)
	elif t == 6 and QtBind.isChecked(gui,cbxEvtMessage_global):
		if QtBind.isChecked(gui,cbxEvtMessage_global):
			searchMessage = QtBind.text(gui,tbxEvtMessage_global_filter)
			if searchMessage:
				try:
					if re.search(searchMessage,msg):
						SendNotify("[Global] **"+player+"** : "+msg)
				except Exception as ex:
					log("Plugin: Error using regex ["+str(ex)+"]")
		else:
			SendNotify("[Global] **"+player+"** : "+msg)
	elif t == 7 and QtBind.isChecked(gui,cbxEvtMessage_notice):
		SendNotify("[Notice] "+msg)
	elif t == 3 and QtBind.isChecked(gui,cbxEvtMessage_gm):
		SendNotify("[GM] **"+player+"** : "+msg)

# All packets received from Silkroad will be passed to this function
# Returning True will keep the packet and False will not forward it to the game server
def handle_joymax(opcode, data):
	if opcode == 0x300C:
		updateType = data[0]
		if updateType == 5:
			if QtBind.isChecked(gui,cbxEvtMessage_uniqueSpawn):
				modelID = struct.unpack_from("<I",data,2)[0]
				uniqueName = get_monster(int(modelID))['name']
				if QtBind.isChecked(gui,cbxEvtMessage_uniqueSpawn_filter):
					searchName = QtBind.text(gui,cbxEvtMessage_uniqueSpawn_filter)
					if searchName:
						try:
							if re.search(searchName,uniqueName):
								SendNotify("["+uniqueName+"] has appeared")
						except Exception as ex:
							log("Plugin: Error using regex ["+str(ex)+"]")
				else:
					SendNotify("["+uniqueName+"] has appeared")
		elif updateType == 6:
			if QtBind.isChecked(gui,cbxEvtMessage_uniqueKilled):
				modelID = struct.unpack_from("<I",data,2)[0]
				killerNameLength = struct.unpack_from('<H', data, 6)[0]
				killerName = struct.unpack_from('<' + str(killerNameLength) + 's', data, 8)[0].decode('cp1252')
				unique = get_monster(int(modelID))
				SendNotify("["+unique['name']+"] killed by ["+killerName+"]")
	elif opcode == 0x34D2:
		if QtBind.isChecked(gui,cbxEvtMessage_battlearena):
			updateType = data[0]
			if updateType == 2:
				SendNotify("[Battle Arena] starts at 15 min.")
			elif updateType == 13:
				SendNotify("[Battle Arena] starts at 5 min.")
			elif updateType == 14:
				SendNotify("[Battle Arena] starts at 1 min.")
			elif updateType == 3:
				SendNotify("[Battle Arena] registration closed")
			elif updateType == 4:
				SendNotify("[Battle Arena] started")
			elif updateType == 5:
				SendNotify("[Battle Arena] finished")
	elif opcode == 0x34B1:
		if QtBind.isChecked(gui,cbxEvtMessage_ctf):
			updateType = data[0]
			if updateType == 2:
				SendNotify("[Capture the Flag] starts at 15 min.")
			elif updateType == 13:
				SendNotify("[Capture the Flag] starts at 5 min.")
			elif updateType == 14:
				SendNotify("[Capture the Flag] starts at 1 min.")
			elif updateType == 3:
				SendNotify("[Capture the Flag] started")
			elif updateType == 9:
				SendNotify("[Capture the Flag] finished")
	elif opcode == 0x30D5:
		if QtBind.isChecked(gui,cbxEvtMessage_quest):
			# Quest update & Quest completed
			if data[0] == 2 and data[10] == 2:
				questID = struct.unpack_from("<I",data,1)[0]
				quest = get_quests()[questID]
				SendNotify("**"+character_data['name']+"** - [Quest] has been completed ["+quest['name']+"]")
	elif opcode == 0xB034:
		# success?
		if data[0] == 1:
			updateType = data[1]
			if updateType == 6: # Ground
				handle_pickup(struct.unpack_from("<I",data,7)[0])
			elif updateType == 17: # Pet
				handle_pickup(struct.unpack_from("<I",data,11)[0])
			elif updateType == 28: # Pet (Full/Quest)
				slotInventory = data[6]
				if slotInventory != 254:
					handle_pickup(struct.unpack_from("<I",data,11)[0])
	return True

def handle_pickup(itemID):
	item = get_item(itemID)
	# check rarity
	if "_RARE" in item["servername"] and QtBind.isChecked(gui,cbxEvtDrop_rare):
		SendNotify("**"+character_data['name']+"** - Item (Rare) picked up ["+item['name']+"]")
	elif QtBind.isChecked(gui,cbxEvtDrop_item):
		SendNotify("**"+character_data['name']+"** - Item picked up ["+item['name']+"]")
	elif item['tid1'] == 1 and QtBind.isChecked(gui,cbxEvtDrop_equip):
		SendNotify("**"+character_data['name']+"** - Item (Equipable) picked up ["+item['name']+"]")
	elif QtBind.isChecked(gui,cbxEvtDrop_filter):
		searchName = QtBind.text(gui,tbxEvtDrop_filter)
		if searchName:
			try:
				if re.search(searchName,item['name']):
					SendNotify("**"+character_data['name']+"** - Item (Filtered) picked up ["+item['name']+"]")
			except Exception as ex:
				log("Plugin: Error using regex ["+str(ex)+"]")

# Create data to send through notify
def CreateInfo(t,data):
	info = {}
	info["type"] = t
	info["data"] = data
	return info

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