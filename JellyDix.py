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
pVersion = '0.2.4'
pUrl = 'https://raw.githubusercontent.com/JellyBitz/phBot-xPlugins/master/JellyDix.py'

# Globals
character_data = None

# Default data
JELLYDIX_KEY="JellyDix"
JELLYDIX_URL="https://jellydix.jellybitz.repl.co"

# Initializing gui_
gui = QtBind.init(__name__,pName)

lblChannels = QtBind.createLabel(gui,"Discord Channel",6,10)
tbxChannels = QtBind.createLineEdit(gui,"",6,25,80,19)
lstChannels = QtBind.createList(gui,6,46,156,212)
btnAddChannel = QtBind.createButton(gui,'btnAddChannel_clicked',"   Add   ",86,25)
btnRemChannel = QtBind.createButton(gui,'btnRemChannel_clicked',"     Remove     ",45,257)
QtBind.createLineEdit(gui,"",169,10,1,257) # Separator line

lblKey = QtBind.createLabel(gui,"Key :",175,10)
tbxKey = QtBind.createLineEdit(gui,JELLYDIX_KEY,205,7,45,19)

lblUrl = QtBind.createLabel(gui,"Website :",260,10)
tbxUrl = QtBind.createLineEdit(gui,JELLYDIX_URL,310,7,155,19)

btnSaveConfig = QtBind.createButton(gui,'saveConfigs',"     Save Changes     ",475,7)
cbxAddTimeStamp = QtBind.createCheckBox(gui,'cbxDoNothing',"Attach timestamps",590,10)

lblTriggers = QtBind.createLabel(gui,"Select the Discord channel to send the notification ( Filters are using regex )",175,35)

# Adding triggers options
lblEvtChar_joined = QtBind.createLabel(gui,'Joined to the game',310,58)
cmbxEvtChar_joined = QtBind.createCombobox(gui,175,55,131,19)

# messages
lblEvtChar_joined = QtBind.createLabel(gui,'Private',310,83)
cmbxEvtMessage_private = QtBind.createCombobox(gui,175,80,131,19)
lblEvtMessage_stall = QtBind.createLabel(gui,'Stall',310,103)
cmbxEvtMessage_stall = QtBind.createCombobox(gui,175,100,131,19)
lblEvtMessage_party = QtBind.createLabel(gui,'Party',310,123)
cmbxEvtMessage_party = QtBind.createCombobox(gui,175,120,131,19)
lblEvtMessage_academy = QtBind.createLabel(gui,'Academy',310,143)
cmbxEvtMessage_academy = QtBind.createCombobox(gui,175,140,131,19)
lblEvtMessageguild = QtBind.createLabel(gui,'Guild',310,163)
cmbxEvtMessage_guild = QtBind.createCombobox(gui,175,160,131,19)
lblEvtMessage_union = QtBind.createLabel(gui,'Union',310,183)
cmbxEvtMessage_union = QtBind.createCombobox(gui,175,180,131,19)
lblEvtMessage_global = QtBind.createLabel(gui,'Global',310,203)
cmbxEvtMessage_global = QtBind.createCombobox(gui,175,200,131,19)
cbxEvtMessage_global_filter = QtBind.createCheckBox(gui,'cbxDoNothing','',175,220)
tbxEvtMessage_global_filter = QtBind.createLineEdit(gui,"",188,220,118,19)
lblEvtMessage_notice = QtBind.createLabel(gui,'Notice',310,243)
cmbxEvtMessage_notice = QtBind.createCombobox(gui,175,240,131,19)
lblEvtMessage_gm = QtBind.createLabel(gui,'GameMaster',310,263)
cmbxEvtMessage_gm = QtBind.createCombobox(gui,175,260,131,19)

# uniques
lblEvtMessage_uniqueSpawn = QtBind.createLabel(gui,'Unique spawn',585,58)
cmbxEvtMessage_uniqueSpawn = QtBind.createCombobox(gui,450,55,131,19)
cbxEvtMessage_uniqueSpawn_filter = QtBind.createCheckBox(gui,'cbxDoNothing','',450,75)
tbxEvtMessage_uniqueSpawn_filter = QtBind.createLineEdit(gui,"",463,75,118,19)
lblEvtMessage_uniqueKilled = QtBind.createLabel(gui,'Unique killed',585,98)
cmbxEvtMessage_uniqueKilled = QtBind.createCombobox(gui,450,95,131,19)

# events
lblEvtMessage_battlearena = QtBind.createLabel(gui,'Battle Arena',585,123)
cmbxEvtMessage_battlearena = QtBind.createCombobox(gui,450,120,131,19)
lblEvtMessage_ctf = QtBind.createLabel(gui,'Capture the Flag',585,143)
cmbxEvtMessage_ctf = QtBind.createCombobox(gui,450,140,131,19)

# picks
lblEvtPick_item = QtBind.createLabel(gui,'Item picked up (vSRO)',585,168)
cmbxEvtPick_item = QtBind.createCombobox(gui,450,165,131,19)
cbxEvtPick_name_filter = QtBind.createCheckBox(gui,'cbxDoNothing','',450,185)
tbxEvtPick_name_filter = QtBind.createLineEdit(gui,"",463,185,118,19)
cbxEvtPick_servername_filter = QtBind.createCheckBox(gui,'cbxDoNothing','',450,205)
tbxEvtPick_servername_filter = QtBind.createLineEdit(gui,"",463,205,118,19)
lblEvtPick_rare = QtBind.createLabel(gui,'Item (Rare) picked up',585,228)
cmbxEvtPick_rare = QtBind.createCombobox(gui,450,225,131,19)
lblEvtPick_equip = QtBind.createLabel(gui,'Item (Equipable) picked up',585,248)
cmbxEvtPick_equip = QtBind.createCombobox(gui,450,245,131,19)

# Initializing GUI(+)
gui_ = QtBind.init(__name__,pName+"(+)")

# warnings
lblEvtNear_unique = QtBind.createLabel(gui_,'Unique near to you',141,10)
cmbxEvtNear_unique = QtBind.createCombobox(gui_,6,7,131,19)
lblEvtNear_hunter = QtBind.createLabel(gui_,'Hunter/Trader near',141,30)
cmbxEvtNear_hunter = QtBind.createCombobox(gui_,6,27,131,19)
lblEvtNear_thief = QtBind.createLabel(gui_,'Thief near',141,50)
cmbxEvtNear_thief = QtBind.createCombobox(gui_,6,47,131,19)
lblEvtChar_attacked = QtBind.createLabel(gui_,'Character attacked',141,70)
cmbxEvtChar_attacked = QtBind.createCombobox(gui_,6,67,131,19)
lblEvtChar_died = QtBind.createLabel(gui_,'Character died',141,90)
cmbxEvtChar_died = QtBind.createCombobox(gui_,6,87,131,19)
lblEvtPet_died = QtBind.createLabel(gui_,'Transport/Horse died',141,110)
cmbxEvtPet_died = QtBind.createCombobox(gui_,6,107,131,19)

lblEvtMessage_quest = QtBind.createLabel(gui_,'Quest completed',416,10)
cmbxEvtMessage_quest = QtBind.createCombobox(gui_,281,7,131,19)

# wrap to iterate
cmbxTriggers={"cmbxEvtChar_joined":cmbxEvtChar_joined,"cmbxEvtMessage_private":cmbxEvtMessage_private,"cmbxEvtMessage_stall":cmbxEvtMessage_stall,"cmbxEvtMessage_party":cmbxEvtMessage_party,"cmbxEvtMessage_academy":cmbxEvtMessage_academy,"cmbxEvtMessage_guild":cmbxEvtMessage_guild,"cmbxEvtMessage_union":cmbxEvtMessage_union,"cmbxEvtMessage_global":cmbxEvtMessage_global,"cmbxEvtMessage_notice":cmbxEvtMessage_notice,"cmbxEvtMessage_gm":cmbxEvtMessage_gm,"cmbxEvtMessage_uniqueSpawn":cmbxEvtMessage_uniqueSpawn,"cmbxEvtMessage_uniqueKilled":cmbxEvtMessage_uniqueKilled,"cmbxEvtMessage_battlearena":cmbxEvtMessage_battlearena,"cmbxEvtMessage_ctf":cmbxEvtMessage_ctf,"cmbxEvtPick_item":cmbxEvtPick_item,"cmbxEvtPick_rare":cmbxEvtPick_rare,"cmbxEvtPick_equip":cmbxEvtPick_equip,"cmbxEvtNear_unique":cmbxEvtNear_unique,"cmbxEvtNear_hunter":cmbxEvtNear_hunter,"cmbxEvtNear_thief":cmbxEvtNear_thief,"cmbxEvtChar_attacked":cmbxEvtChar_attacked,"cmbxEvtChar_died":cmbxEvtChar_died,"cmbxEvtPet_died":cmbxEvtPet_died}
cmbxTriggers_={"cmbxEvtNear_unique":cmbxEvtNear_unique,"cmbxEvtNear_hunter":cmbxEvtNear_hunter,"cmbxEvtNear_thief":cmbxEvtNear_thief,"cmbxEvtChar_attacked":cmbxEvtChar_attacked,"cmbxEvtChar_died":cmbxEvtChar_died,"cmbxEvtPet_died":cmbxEvtPet_died,"cmbxEvtMessage_quest":cmbxEvtMessage_quest}

# Return folder path
def getPath():
	return get_config_dir()+pName+"\\"

# Return character configs path (JSON)
def getConfig():
	return getPath()+character_data['server'] + "_" + character_data['name'] + ".json"

# Load default configs
def loadDefaultConfig():
	# Clear data
	QtBind.setText(gui,tbxChannels,"")
	QtBind.clear(gui,lstChannels)

	QtBind.setText(gui,tbxKey,JELLYDIX_KEY)
	QtBind.setText(gui,tbxUrl,JELLYDIX_URL)

	QtBind.setChecked(gui,cbxAddTimeStamp,False)
	
	# Reset triggers
	for name,cmbx in cmbxTriggers.items():
		QtBind.clear(gui,cmbx)
		QtBind.append(gui,cmbx,"")

	QtBind.setChecked(gui,cbxEvtMessage_global_filter,False)
	QtBind.setText(gui,tbxEvtMessage_global_filter," Filter by message")

	QtBind.setChecked(gui,cbxEvtMessage_uniqueSpawn_filter,False)
	QtBind.setText(gui,tbxEvtMessage_uniqueSpawn_filter," Filter by name")

	QtBind.setChecked(gui,cbxEvtPick_name_filter,False)
	QtBind.setText(gui,tbxEvtPick_name_filter," Filter by name")
	QtBind.setChecked(gui,cbxEvtPick_servername_filter,False)
	QtBind.setText(gui,tbxEvtPick_servername_filter," Filter by servername")

	for name,cmbx in cmbxTriggers_.items():
		QtBind.clear(gui_,cmbx)
		QtBind.append(gui_,cmbx,"")

# Save specific value at config
def saveConfigs():
	# Save if data has been loaded
	if isJoined():
		# Save all data
		data = {}
		data["Channels"] = QtBind.getItems(gui,lstChannels)

		data["Key"] = QtBind.text(gui,tbxKey)
		data["Url"] = QtBind.text(gui,tbxUrl)

		data["AddTimeStamp"] = QtBind.isChecked(gui,cbxAddTimeStamp)
		
		# Save triggers from tabs
		triggers = {}
		data["Triggers"] = triggers

		for name,cmbx in cmbxTriggers.items():
			triggers[name] = QtBind.text(gui,cmbx)

		triggers["cbxEvtMessage_global_filter"] = QtBind.isChecked(gui,cbxEvtMessage_global_filter)
		triggers["tbxEvtMessage_global_filter"] = QtBind.text(gui,tbxEvtMessage_global_filter)

		triggers["cbxEvtMessage_uniqueSpawn_filter"] = QtBind.isChecked(gui,cbxEvtMessage_uniqueSpawn_filter)
		triggers["tbxEvtMessage_uniqueSpawn_filter"] = QtBind.text(gui,tbxEvtMessage_uniqueSpawn_filter)

		triggers["cbxEvtPick_name_filter"] = QtBind.isChecked(gui,cbxEvtPick_name_filter)
		triggers["tbxEvtPick_name_filter"] = QtBind.text(gui,tbxEvtPick_name_filter)
		triggers["cbxEvtPick_servername_filter"] = QtBind.isChecked(gui,cbxEvtPick_servername_filter)
		triggers["tbxEvtPick_servername_filter"] = QtBind.text(gui,tbxEvtPick_servername_filter)

		for name,cmbx in cmbxTriggers_.items():
			triggers[name] = QtBind.text(gui_,cmbx)

		# Overrides
		with open(getConfig(),"w") as f:
			f.write(json.dumps(data, indent=4, sort_keys=True))
		log("Plugin: "+pName+" config is now saved!")

# Loads all config previously saved
def loadConfigs():
	loadDefaultConfig()
	if isJoined():
		# Check config exists to load
		if os.path.exists(getConfig()):
			data = {}
			with open(getConfig(),"r") as f:
				data = json.load(f)
			# Load channels
			if "Channels" in data:
				for channel_id in data["Channels"]:
					QtBind.append(gui,lstChannels,channel_id)
					for name,cmbx in cmbxTriggers.items():
						QtBind.append(gui,cmbx,channel_id)
					for name,cmbx in cmbxTriggers_.items():
						QtBind.append(gui_,cmbx,channel_id)

			if "Key" in data:
				QtBind.setText(gui,tbxKey,data["Key"])
			if "Url" in data:
				QtBind.setText(gui,tbxUrl,data["Url"])

			if "AddTimeStamp" in data and data["AddTimeStamp"]:
				QtBind.setChecked(gui,cbxAddTimeStamp,True)

			# Load triggers
			if "Triggers" in data:
				triggers = data["Triggers"]

				if "cmbxEvtChar_joined" in triggers:
					QtBind.setText(gui,cmbxEvtChar_joined,triggers["cmbxEvtChar_joined"])

				if "cmbxEvtMessage_private" in triggers:
					QtBind.setText(gui,cmbxEvtMessage_private,triggers["cmbxEvtMessage_private"])
				if "cmbxEvtMessage_stall" in triggers:
					QtBind.setText(gui,cmbxEvtMessage_stall,triggers["cmbxEvtMessage_stall"])
				if "cmbxEvtMessage_party" in triggers:
					QtBind.setText(gui,cmbxEvtMessage_party,triggers["cmbxEvtMessage_party"])
				if "cmbxEvtMessage_academy" in triggers:
					QtBind.setText(gui,cmbxEvtMessage_academy,triggers["cmbxEvtMessage_academy"])
				if "cmbxEvtMessage_guild" in triggers:
					QtBind.setText(gui,cmbxEvtMessage_guild,triggers["cmbxEvtMessage_guild"])
				if "cmbxEvtMessage_union" in triggers:
					QtBind.setText(gui,cmbxEvtMessage_union,triggers["cmbxEvtMessage_union"])
				if "cmbxEvtMessage_global" in triggers:
					QtBind.setText(gui,cmbxEvtMessage_global,triggers["cmbxEvtMessage_global"])
				if "cbxEvtMessage_global_filter" in triggers and triggers["cbxEvtMessage_global_filter"]:
					QtBind.setChecked(gui,cbxEvtMessage_global_filter,True)
				if "tbxEvtMessage_global_filter" in triggers and triggers["tbxEvtMessage_global_filter"]:
					QtBind.setText(gui,tbxEvtMessage_global_filter,triggers["tbxEvtMessage_global_filter"])
				if "cmbxEvtMessage_notice" in triggers:
					QtBind.setText(gui,cmbxEvtMessage_notice,triggers["cmbxEvtMessage_notice"])
				if "cmbxEvtMessage_gm" in triggers:
					QtBind.setText(gui,cmbxEvtMessage_gm,triggers["cmbxEvtMessage_gm"])

				if "cmbxEvtMessage_uniqueSpawn" in triggers:
					QtBind.setText(gui,cmbxEvtMessage_uniqueSpawn,triggers["cmbxEvtMessage_uniqueSpawn"])
				if "cbxEvtMessage_uniqueSpawn_filter" in triggers and triggers["cbxEvtMessage_uniqueSpawn_filter"]:
					QtBind.setChecked(gui,cbxEvtMessage_uniqueSpawn_filter,True)
				if "tbxEvtMessage_uniqueSpawn_filter" in triggers and triggers["tbxEvtMessage_uniqueSpawn_filter"]:
					QtBind.setText(gui,tbxEvtMessage_uniqueSpawn_filter,triggers["tbxEvtMessage_uniqueSpawn_filter"])
				if "cmbxEvtMessage_uniqueKilled" in triggers:
					QtBind.setText(gui,cmbxEvtMessage_uniqueKilled,triggers["cmbxEvtMessage_uniqueKilled"])

				if "cmbxEvtMessage_battlearena" in triggers:
					QtBind.setText(gui,cmbxEvtMessage_battlearena,triggers["cmbxEvtMessage_battlearena"])
				if "cmbxEvtMessage_ctf" in triggers:
					QtBind.setText(gui,cmbxEvtMessage_ctf,triggers["cmbxEvtMessage_ctf"])

				if "cmbxEvtPick_item" in triggers:
					QtBind.setText(gui,cmbxEvtPick_item,triggers["cmbxEvtPick_item"])
				if "cbxEvtPick_name_filter" in triggers and triggers["cbxEvtPick_name_filter"]:
					QtBind.setChecked(gui,cbxEvtPick_name_filter,True)
				if "tbxEvtPick_name_filter" in triggers and triggers["tbxEvtPick_name_filter"]:
					QtBind.setText(gui,tbxEvtPick_name_filter,triggers["tbxEvtPick_name_filter"])
				if "cbxEvtPick_servername_filter" in triggers and triggers["cbxEvtPick_servername_filter"]:
					QtBind.setChecked(gui,cbxEvtPick_servername_filter,True)
				if "tbxEvtPick_servername_filter" in triggers and triggers["tbxEvtPick_servername_filter"]:
					QtBind.setText(gui,tbxEvtPick_servername_filter,triggers["tbxEvtPick_servername_filter"])
				if "cmbxEvtPick_rare" in triggers:
					QtBind.setText(gui,cmbxEvtPick_rare,triggers["cmbxEvtPick_rare"])
				if "cmbxEvtPick_equip" in triggers:
					QtBind.setText(gui,cmbxEvtPick_equip,triggers["cmbxEvtPick_equip"])

				if "cmbxEvtNear_unique" in triggers:
					QtBind.setText(gui_,cmbxEvtNear_unique,triggers["cmbxEvtNear_unique"])
				if "cmbxEvtNear_hunter" in triggers:
					QtBind.setText(gui_,cmbxEvtNear_hunter,triggers["cmbxEvtNear_hunter"])
				if "cmbxEvtNear_thief" in triggers:
					QtBind.setText(gui_,cmbxEvtNear_thief,triggers["cmbxEvtNear_thief"])
				if "cmbxEvtChar_attacked" in triggers:
					QtBind.setText(gui_,cmbxEvtChar_attacked,triggers["cmbxEvtChar_attacked"])
				if "cmbxEvtChar_died" in triggers:
					QtBind.setText(gui_,cmbxEvtChar_died,triggers["cmbxEvtChar_died"])
				if "cmbxEvtPet_died" in triggers:
					QtBind.setText(gui_,cmbxEvtPet_died,triggers["cmbxEvtPet_died"])

				if "cmbxEvtMessage_quest" in triggers:
					QtBind.setText(gui_,cmbxEvtMessage_quest,triggers["cmbxEvtMessage_quest"])

# Checkbox trigger clicked
def cbxDoNothing(checked):
	pass

# Return True if the text exist at the array
def ListContains(list,text):
	text = text.lower()
	for i in range(len(list)):
		if list[i].lower() == text:
			return True
	return False

# Add discord channel
def btnAddChannel_clicked():
	if isJoined():
		channel_id = QtBind.text(gui,tbxChannels)
		if channel_id and channel_id.isnumeric():
			# channel it's not empty and not added
			if not ListContains(QtBind.getItems(gui,lstChannels),channel_id):
				# init dict
				data = {}
				# Load config
				if os.path.exists(getConfig()):
					with open(getConfig(), 'r') as f:
						data = json.load(f)
				# Add new channel
				if not "Channels" in data:
					data['Channels'] = []
				data["Channels"].append(channel_id)
				# Replace configs
				with open(getConfig(),"w") as f:
					f.write(json.dumps(data, indent=4, sort_keys=True))
				
				# Add new channel on everything
				QtBind.append(gui,lstChannels,channel_id)
				for name,cmbx in cmbxTriggers.items():
					QtBind.append(gui,cmbx,channel_id)
				for name,cmbx in cmbxTriggers_.items():
					QtBind.append(gui_,cmbx,channel_id)

				QtBind.setText(gui,tbxChannels,"")
				log('Plugin: Channel added ['+channel_id+']')
		else:
			log('Plugin: Error, The channel must be an identifier number!')

# Remove discord channel
def btnRemChannel_clicked():
	if isJoined():
		channelItem = QtBind.text(gui,lstChannels)
		if channelItem:
			# Remove channel from all combo's
			for name,cmbx in cmbxTriggers.items():
				channelReset = False
				if QtBind.text(gui,cmbx) == channelItem:
					channelReset = True
				QtBind.remove(gui,cmbx,channelItem)
				if channelReset:
					QtBind.setText(gui,cmbx,"")
			for name,cmbx in cmbxTriggers_.items():
				channelReset = False
				if QtBind.text(gui_,cmbx) == channelItem:
					channelReset = True
				QtBind.remove(gui_,cmbx,channelItem)
				if channelReset:
					QtBind.setText(gui_,cmbx,"")
			# Update config file
			if os.path.exists(getConfig()):
				data = {"Channels":[]}
				with open(getConfig(), 'r') as f:
					data = json.load(f)
				# try to remove channel from config file
				try:
					data["Channels"].remove(channelItem)
					with open(getConfig(),"w") as f:
						f.write(json.dumps(data, indent=4, sort_keys=True))
				except:
					pass
			QtBind.remove(gui,lstChannels,channelItem)
			log('Plugin: Channel removed ['+channelItem+']')

# Create an info package to send through notify
def CreateInfo(t,data):
	info = {}
	info["type"] = t
	info["data"] = data
	return info

# Send a notification to discord channel
# message : Text shown as discord notification
# channel_id : ID from channel to be sent
# info : Extra data used at server for some notifications
def Notify(channel_id,message,info=None):
	# Check if there is enough data to create a notification
	if not channel_id or not message:
		return
	key = QtBind.text(gui,tbxKey)
	url = QtBind.text(gui,tbxUrl)
	if not key or not url:
		return
	# Try to send notification
	try:
		# Add timestamp
		if QtBind.isChecked(gui,cbxAddTimeStamp):
			message = "||"+datetime.now().strftime('%H:%M:%S')+"|| "+message
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
				if msg == 'true' or msg == 'success':
					log("Plugin: notify sent to Discord!")
				else:
					log("Plugin: notify failed ["+msg+"]")
			except Exception as ex2:
				log("Plugin: Error reading response from server ["+str(ex2)+"]")
	except Exception as ex:
		log("Plugin: Error loading url ["+str(ex)+"]")

# Check if character is ingame
def isJoined():
	global character_data
	character_data = get_character_data()
	if character_data and "name" in character_data and character_data["name"]:
		return True
	return False

# Called when the character enters the game world
def joined_game():
	loadConfigs()
	Notify(QtBind.text(gui,cmbxEvtChar_joined),"|`"+character_data['name']+"`| - Joined to the game")

# All chat messages received are sent to this function
def handle_chat(t,player,msg):
	# Check message type
	if t == 2:
		Notify(QtBind.text(gui,cmbxEvtMessage_private),"|`"+character_data['name']+"`| - [**Private**] from `"+player+"`: "+msg)
	elif t == 9:
		Notify(QtBind.text(gui,cmbxEvtMessage_stall),"|`"+character_data['name']+"`| - [**Stall**] from `"+player+"`: "+msg)
	elif t == 4:
		Notify(QtBind.text(gui,cmbxEvtMessage_party),"|`"+character_data['name']+"`| - "+"[**Party**] `"+player+"`: "+msg)
	elif t == 16:
		Notify(QtBind.text(gui,cmbxEvtMessage_academy),"|`"+character_data['name']+"`| - "+"[**Academy**] `"+player+"`: "+msg)
	elif t == 5:
		Notify(QtBind.text(gui,cmbxEvtMessage_guild),"[**Guild**] `"+player+"`: "+msg)
	elif t == 11:
		Notify(QtBind.text(gui,cmbxEvtMessage_union),"[**Union**] `"+player+"`: "+msg)
	elif t == 6:
		if QtBind.isChecked(gui,cbxEvtMessage_global_filter):
			searchMessage = QtBind.text(gui,tbxEvtMessage_global_filter)
			if searchMessage:
				try:
					if re.search(searchMessage,msg):
						Notify(QtBind.text(gui,cmbxEvtMessage_global),"[**Global**] `"+player+"`: "+msg)
				except Exception as ex:
					log("Plugin: Error at regex ["+str(ex)+"]")
		else:
			Notify(QtBind.text(gui,cmbxEvtMessage_global),"[**Global**] `"+player+"`: "+msg)
	elif t == 7:
		Notify(QtBind.text(gui,cmbxEvtMessage_notice),"[**Notice**] : "+msg)
	elif t == 3:
		Notify(QtBind.text(gui,cmbxEvtMessage_gm),"[**GameMaster**] `"+player+"`: "+msg)

# Called for specific events. data field will always be a string.
def handle_event(t, data):
	# Filter events
	if t == 0:
		Notify(QtBind.text(gui_,cmbxEvtNear_unique),"|`"+character_data['name']+"`| - **"+data+"** unique is near to you!",CreateInfo("position",get_position()))
	elif t == 1:
		Notify(QtBind.text(gui_,cmbxEvtNear_hunter),"|`"+character_data['name']+"`| - **Hunter/Trader** `"+data+"` is near to you!",CreateInfo("position",get_position()))
	elif t == 2:
		Notify(QtBind.text(gui_,cmbxEvtNear_thief),"|`"+character_data['name']+"`| - **Thief** `"+data+"` is near to you!",CreateInfo("position",get_position()))
	elif t == 4:
		Notify(QtBind.text(gui_,cmbxEvtChar_died),"|`"+character_data['name']+"`| - `"+data+"` is attacking you!")
	elif t == 3:
		t = get_pets()[data]
		Notify(QtBind.text(gui_,cmbxEvtChar_attacked),"|`"+character_data['name']+"`| - **"+(t['type'].title())+"** pet died")
	elif t == 7:
		Notify(QtBind.text(gui_,cmbxEvtPet_died),"|`"+character_data['name']+"`| - You died",CreateInfo("position",get_position()))

# All packets received from Silkroad will be passed to this function
# Returning True will keep the packet and False will not forward it to the game server
def handle_joymax(opcode, data):
	if opcode == 0x300C:
		updateType = data[0]
		if updateType == 5:
			channel_id = QtBind.text(gui,cmbxEvtMessage_uniqueSpawn)
			if channel_id:
				modelID = struct.unpack_from("<I",data,2)[0]
				uniqueName = get_monster(int(modelID))['name']
				if QtBind.isChecked(gui,cbxEvtMessage_uniqueSpawn_filter):
					searchName = QtBind.text(gui,tbxEvtMessage_uniqueSpawn_filter)
					if searchName:
						try:
							if re.search(searchName,uniqueName):
								Notify(channel_id,"**"+uniqueName+"** has appeared")
						except Exception as ex:
							log("Plugin: Error at regex ["+str(ex)+"]")
				else:
					Notify(channel_id,"**"+uniqueName+"** has appeared")
		elif updateType == 6:
			channel_id = QtBind.text(gui,cmbxEvtMessage_uniqueKilled)
			if channel_id:
				modelID = struct.unpack_from("<I",data,2)[0]
				killerNameLength = struct.unpack_from('<H', data, 6)[0]
				killerName = struct.unpack_from('<' + str(killerNameLength) + 's', data, 8)[0].decode('cp1252')
				unique = get_monster(int(modelID))
				Notify(channel_id,"**"+unique['name']+"** killed by `"+killerName+"`")
	elif opcode == 0x34D2:
		channel_id = QtBind.text(gui,cmbxEvtMessage_battlearena)
		if channel_id:
			updateType = data[0]
			if updateType == 2:
				Notify(channel_id,"**Battle Arena** starts at 15 min.")
			elif updateType == 13:
				Notify(channel_id,"**Battle Arena** starts at 5 min.")
			elif updateType == 14:
				Notify(channel_id,"**Battle Arena** starts at 1 min.")
			elif updateType == 3:
				Notify(channel_id,"**Battle Arena** registration closed")
			elif updateType == 4:
				Notify(channel_id,"**Battle Arena** started")
			elif updateType == 5:
				Notify(channel_id,"**Battle Arena** finished")
	elif opcode == 0x34B1:
		channel_id = QtBind.text(gui,cmbxEvtMessage_ctf)
		if channel_id:
			updateType = data[0]
			if updateType == 2:
				Notify(channel_id,"**Capture the Flag** starts at 15 min.")
			elif updateType == 13:
				Notify(channel_id,"**Capture the Flag** starts at 5 min.")
			elif updateType == 14:
				Notify(channel_id,"**Capture the Flag** starts at 1 min.")
			elif updateType == 3:
				Notify(channel_id,"**Capture the Flag** started")
			elif updateType == 9:
				Notify(channel_id,"**Capture the Flag** finished")
	elif opcode == 0x30D5:
		channel_id = QtBind.text(gui_,cmbxEvtMessage_quest)
		if channel_id:
			# Quest update & Quest completed
			if data[0] == 2 and data[10] == 2:
				questID = struct.unpack_from("<I",data,1)[0]
				quest = get_quests()[questID]
				Notify(channel_id,"|`"+character_data['name']+"`| - **Quest** has been completed ***"+quest['name']+"***")
	elif opcode == 0xB034:
		try:
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
		except:
			log("Plugin: Oops! Pick up parsing error..")
			log("If you want support, send me all this via private message:")
			log("Data [" + ("None" if not data else ' '.join('{:02X}'.format(x) for x in data))+"]\nLocale ["+str(get_locale())+"]")
	return True

# All picked up items are sent to this function (only vSRO working at the moment) 
def handle_pickup(itemID):
	item = get_item(itemID)
	# check rarity
	if "_RARE" in item["servername"]:
		channel_id = QtBind.text(gui_,cmbxEvtPick_rare)
		if channel_id:
			Notify(channel_id,"|`"+character_data['name']+"`| - Item (Rare) picked up ***"+item['name']+"***")
			return
	# check equipable
	if item['tid1'] == 1:
		channel_id = QtBind.text(gui_,cmbxEvtPick_equip)
		if channel_id:
			Notify(channel_id,"|`"+character_data['name']+"`| - Item (Equipable) picked up ***"+item['name']+"***")
			return

	channel_id = QtBind.text(gui_,cmbxEvtPick_item)
	if channel_id:
		# check filter name
		if QtBind.isChecked(gui_,cbxEvtPick_name_filter):
			searchName = QtBind.text(gui_,tbxEvtPick_name_filter)
			if searchName:
				try:
					if re.search(searchName,item['name']):
						Notify(channel_id,"|`"+character_data['name']+"`| - Item (Filtered) picked up ***"+item['name']+"***")
						return
				except Exception as ex:
					log("Plugin: Error at regex ["+str(ex)+"]")
		# check filter servername
		if QtBind.isChecked(gui_,cbxEvtPick_servername_filter):
			searchServername = QtBind.text(gui_,tbxEvtPick_servername_filter)
			if searchServername:
				try:
					if re.search(searchServername,item['servername']):
						Notify(channel_id,"|`"+character_data['name']+"`| - Item (Filtered) picked up ***"+item['name']+"***")
						return
				except Exception as ex:
					log("Plugin: Error at regex ["+str(ex)+"]")

# Plugin load success
log('Plugin: '+pName+' v'+pVersion+' successfully loaded')

# Creating configs folder
if not os.path.exists(getPath()):
	os.makedirs(getPath())
	log('Plugin: '+pName+' folder has been created')

# Adding RELOAD plugin support
loadConfigs()