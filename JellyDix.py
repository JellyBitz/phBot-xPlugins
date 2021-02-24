from phBot import *
import QtBind
from datetime import datetime
from threading import Timer
import urllib.request
import urllib.parse
import struct
import json
import time
import os
import re

pName = 'JellyDix'
pVersion = '2.11.0'
pUrl = 'https://raw.githubusercontent.com/JellyBitz/phBot-xPlugins/master/JellyDix.py'

# ______________________________ Initializing ______________________________ #

URL_HOST = "https://jellydix.ddns.net" # API server
URL_REQUEST_TIMEOUT = 15 # sec
DISCORD_FETCH_DELAY = 5000 # ms

# Globals
character_data = None
party_data = None
chat_data = {}
isOnline = False
hasStall = False

discord_fetch_counter = 0
discord_chat_handlers = []

# Graphic user interface
gui = QtBind.init(__name__,pName)

QtBind.createLabel(gui,"Discord Channels ID",6,10)
tbxChannels = QtBind.createLineEdit(gui,"",6,25,80,19)
lstChannels = QtBind.createList(gui,6,46,156,90)
btnAddChannel = QtBind.createButton(gui,'btnAddChannel_clicked',"   Add   ",86,25)
btnRemChannel = QtBind.createButton(gui,'btnRemChannel_clicked',"     Remove     ",45,135)

# Discord options
QtBind.createLabel(gui,"Token :",6,165)
tbxToken = QtBind.createLineEdit(gui,"",43,163,119,19)

cbxAddTimestamp = QtBind.createCheckBox(gui,'cbxDoNothing','Add phBot timestamp',6,185)
cbxDiscord_interactions = QtBind.createCheckBox(gui,'cbxDoNothing','Use Discord interactions',6,205)
tbxDiscord_guild_id = QtBind.createLineEdit(gui,'',6,225,145,19)
cbxDiscord_check_all = QtBind.createCheckBox(gui,'cbxDoNothing','Check all interactions',6,245)

# Separator line
QtBind.createLineEdit(gui,"",169,10,1,262)

# Triggers
QtBind.createLabel(gui,"Select the Discord channel to send the notification ( Filters are using regex! )",175,10)
btnSaveConfig = QtBind.createButton(gui,'saveConfigs',"     Save Changes     ",615,4)

# Creating margins to locate all quickly
_x = 180
_y = 30
_Height = 19
_cmbxWidth = 131
_tbxWidth = 118

# login states
QtBind.createLabel(gui,'Joined to the game',_x+_cmbxWidth+4,_y+3)
cmbxEvtChar_joined = QtBind.createCombobox(gui,_x,_y,_cmbxWidth,_Height)
_y+=20
QtBind.createLabel(gui,'Disconnected from game',_x+_cmbxWidth+4,_y+3)
cmbxEvtChar_disconnected = QtBind.createCombobox(gui,_x,_y,_cmbxWidth,_Height)
_y+=20

# uniques
_y += 5
QtBind.createLabel(gui,'Unique spawn',_x+_cmbxWidth+4,_y+3)
cmbxEvtMessage_uniqueSpawn = QtBind.createCombobox(gui,_x,_y,_cmbxWidth,_Height)
_y+=20
cbxEvtMessage_uniqueSpawn_filter = QtBind.createCheckBox(gui,'cbxDoNothing','',_x,_y+3)
tbxEvtMessage_uniqueSpawn_filter = QtBind.createLineEdit(gui,"",_x+13,_y,_tbxWidth,_Height)
_y+=20
QtBind.createLabel(gui,'Unique killed',_x+_cmbxWidth+4,_y+3)
cmbxEvtMessage_uniqueKilled = QtBind.createCombobox(gui,_x,_y,_cmbxWidth,_Height)
_y+=20
cbxEvtMessage_uniqueKilled_filter = QtBind.createCheckBox(gui,'cbxDoNothing','',_x,_y+3)
tbxEvtMessage_uniqueKilled_filter = QtBind.createLineEdit(gui,"",_x+13,_y,_tbxWidth,_Height)
_y+=20

# events
_y += 5
QtBind.createLabel(gui,'Capture the Flag',_x+_cmbxWidth+4,_y+3)
cmbxEvtMessage_ctf = QtBind.createCombobox(gui,_x,_y,_cmbxWidth,_Height)
_y+=20
QtBind.createLabel(gui,'Battle Arena',_x+_cmbxWidth+4,_y+3)
cmbxEvtMessage_battlearena = QtBind.createCombobox(gui,_x,_y,_cmbxWidth,_Height)
_y+=20
QtBind.createLabel(gui,'Fortress War',_x+_cmbxWidth+4,_y+3)
cmbxEvtMessage_fortress = QtBind.createCombobox(gui,_x,_y,_cmbxWidth,_Height)
_y+=20
QtBind.createLabel(gui,'Consignment Hunter',_x+_cmbxWidth+4,_y+3)
cmbxEvtMessage_consignmenthunter = QtBind.createCombobox(gui,_x,_y,_cmbxWidth,_Height)
_y+=20
QtBind.createLabel(gui,'Consignment Thief',_x+_cmbxWidth+4,_y+3)
cmbxEvtMessage_consignmentthief = QtBind.createCombobox(gui,_x,_y,_cmbxWidth,_Height)

# warnings
_x += _cmbxWidth * 2 + 10
_y = 30
QtBind.createLabel(gui,'GM near to you',_x+_cmbxWidth+4,_y+3)
cmbxEvtNear_gm = QtBind.createCombobox(gui,_x,_y,_cmbxWidth,_Height)
_y+=20
QtBind.createLabel(gui,'Unique near to you',_x+_cmbxWidth+4,_y+3)
cmbxEvtNear_unique = QtBind.createCombobox(gui,_x,_y,_cmbxWidth,_Height)
_y+=20
QtBind.createLabel(gui,'Hunter/Trader near',_x+_cmbxWidth+4,_y+3)
cmbxEvtNear_hunter = QtBind.createCombobox(gui,_x,_y,_cmbxWidth,_Height)
_y+=20
QtBind.createLabel(gui,'Thief near',_x+_cmbxWidth+4,_y+3)
cmbxEvtNear_thief = QtBind.createCombobox(gui,_x,_y,_cmbxWidth,_Height)
_y+=20
QtBind.createLabel(gui,'Character attacked',_x+_cmbxWidth+4,_y+3)
cmbxEvtChar_attacked = QtBind.createCombobox(gui,_x,_y,_cmbxWidth,_Height)
_y+=20
QtBind.createLabel(gui,'Character died',_x+_cmbxWidth+4,_y+3)
cmbxEvtChar_died = QtBind.createCombobox(gui,_x,_y,_cmbxWidth,_Height)
_y+=20
QtBind.createLabel(gui,'Transport/Horse died',_x+_cmbxWidth+4,_y+3)
cmbxEvtPet_died = QtBind.createCombobox(gui,_x,_y,_cmbxWidth,_Height)
_y+=20

# misc
_y+=5
QtBind.createLabel(gui,'Quest completed',_x+_cmbxWidth+4,_y+3)
cmbxEvtMessage_quest = QtBind.createCombobox(gui,_x,_y,_cmbxWidth,_Height)
_y+=20
QtBind.createLabel(gui,'Alchemy completed',_x+_cmbxWidth+4,_y+3)
cmbxEvtBot_alchemy = QtBind.createCombobox(gui,_x,_y,_cmbxWidth,_Height)
_y+=20
QtBind.createLabel(gui,'Stall item sold',_x+_cmbxWidth+4,_y+3)
cmbxEvtMessage_item_sold = QtBind.createCombobox(gui,_x,_y,_cmbxWidth,_Height)
_y+=20

# wrap to iterate
cmbxTriggers={'cmbxEvtChar_joined':cmbxEvtChar_joined,'cmbxEvtChar_disconnected':cmbxEvtChar_disconnected,'cmbxEvtMessage_uniqueSpawn':cmbxEvtMessage_uniqueSpawn,'cmbxEvtMessage_uniqueKilled':cmbxEvtMessage_uniqueKilled,'cmbxEvtMessage_ctf':cmbxEvtMessage_ctf,'cmbxEvtMessage_battlearena':cmbxEvtMessage_battlearena,'cmbxEvtMessage_fortress':cmbxEvtMessage_fortress,'cmbxEvtMessage_consignmenthunter':cmbxEvtMessage_consignmenthunter,'cmbxEvtMessage_consignmentthief':cmbxEvtMessage_consignmentthief,'cmbxEvtNear_gm':cmbxEvtNear_gm,'cmbxEvtNear_unique':cmbxEvtNear_unique,'cmbxEvtNear_hunter':cmbxEvtNear_hunter,'cmbxEvtNear_thief':cmbxEvtNear_thief,'cmbxEvtChar_attacked':cmbxEvtChar_attacked,'cmbxEvtChar_died':cmbxEvtChar_died,'cmbxEvtPet_died':cmbxEvtPet_died,'cmbxEvtMessage_quest':cmbxEvtMessage_quest,'cmbxEvtBot_alchemy':cmbxEvtBot_alchemy,'cmbxEvtMessage_item_sold':cmbxEvtMessage_item_sold}

# Graphic user interface (+)
gui_ = QtBind.init(__name__,pName+"(+)")

# Creating margins to locate columns quickly
_x = 6
_y = 7
_cmbxWidth = 131
_tbxWidth = 118

# chat messages
QtBind.createLabel(gui_,'General',_x+_cmbxWidth+4,_y+3)
cmbxEvtMessage_all = QtBind.createCombobox(gui_,_x,_y,_cmbxWidth,_Height)
_y+=20
QtBind.createLabel(gui_,'Private',_x+_cmbxWidth+4,_y+3)
cmbxEvtMessage_private = QtBind.createCombobox(gui_,_x,_y,_cmbxWidth,_Height)
_y+=20
QtBind.createLabel(gui_,'Stall',_x+_cmbxWidth+4,_y+3)
cmbxEvtMessage_stall = QtBind.createCombobox(gui_,_x,_y,_cmbxWidth,_Height)
_y+=20
QtBind.createLabel(gui_,'Party',_x+_cmbxWidth+4,_y+3)
cmbxEvtMessage_party = QtBind.createCombobox(gui_,_x,_y,_cmbxWidth,_Height)
_y+=20
QtBind.createLabel(gui_,'Academy',_x+_cmbxWidth+4,_y+3)
cmbxEvtMessage_academy = QtBind.createCombobox(gui_,_x,_y,_cmbxWidth,_Height)
_y+=20
QtBind.createLabel(gui_,'Guild',_x+_cmbxWidth+4,_y+3)
cmbxEvtMessage_guild = QtBind.createCombobox(gui_,_x,_y,_cmbxWidth,_Height)
_y+=20
QtBind.createLabel(gui_,'Union',_x+_cmbxWidth+4,_y+3)
cmbxEvtMessage_union = QtBind.createCombobox(gui_,_x,_y,_cmbxWidth,_Height)
_y+=20
QtBind.createLabel(gui_,'Global',_x+_cmbxWidth+4,_y+3)
cmbxEvtMessage_global = QtBind.createCombobox(gui_,_x,_y,_cmbxWidth,_Height)
_y+=20
cbxEvtMessage_global_filter = QtBind.createCheckBox(gui_,'cbxDoNothing','',_x,_y+3)
tbxEvtMessage_global_filter = QtBind.createLineEdit(gui_,"",_x+13,_y,_tbxWidth,_Height)
_y+=20
QtBind.createLabel(gui_,'Notice',_x+_cmbxWidth+4,_y+3)
cmbxEvtMessage_notice = QtBind.createCombobox(gui_,_x,_y,_cmbxWidth,_Height)
_y+=20
cbxEvtMessage_notice_filter = QtBind.createCheckBox(gui_,'cbxDoNothing','',_x,_y+3)
tbxEvtMessage_notice_filter = QtBind.createLineEdit(gui_,"",_x+13,_y,_tbxWidth,_Height)
_y+=20
QtBind.createLabel(gui_,'GM Talk',_x+_cmbxWidth+4,_y+3)
cmbxEvtMessage_gm = QtBind.createCombobox(gui_,_x,_y,_cmbxWidth,_Height)

# party
_x += int(_cmbxWidth*1.5) 
_y = 7
QtBind.createLabel(gui_,'Party joined',_x+_cmbxWidth+4,_y+3)
cmbxEvtParty_joined = QtBind.createCombobox(gui_,_x,_y,_cmbxWidth,_Height)
_y+=20
QtBind.createLabel(gui_,'Party left',_x+_cmbxWidth+4,_y+3)
cmbxEvtParty_left = QtBind.createCombobox(gui_,_x,_y,_cmbxWidth,_Height)
_y+=20
QtBind.createLabel(gui_,'Party member joined',_x+_cmbxWidth+4,_y+3)
cmbxEvtParty_memberJoin = QtBind.createCombobox(gui_,_x,_y,_cmbxWidth,_Height)
_y+=20
QtBind.createLabel(gui_,'Party member left',_x+_cmbxWidth+4,_y+3)
cmbxEvtParty_memberLeft = QtBind.createCombobox(gui_,_x,_y,_cmbxWidth,_Height)
_y+=20
QtBind.createLabel(gui_,'Party member level up',_x+_cmbxWidth+4,_y+3)
cmbxEvtParty_memberLvlUp = QtBind.createCombobox(gui_,_x,_y,_cmbxWidth,_Height)
_y+=20

# guild
_y+=5
QtBind.createLabel(gui_,'Guild notice changed',_x+_cmbxWidth+4,_y+3)
cmbxEvtGuild_noticechanged = QtBind.createCombobox(gui_,_x,_y,_cmbxWidth,_Height)
_y+=20
QtBind.createLabel(gui_,'Guild member login',_x+_cmbxWidth+4,_y+3)
cmbxEvtGuild_memberLogin = QtBind.createCombobox(gui_,_x,_y,_cmbxWidth,_Height)
_y+=20
QtBind.createLabel(gui_,'Guild member logout',_x+_cmbxWidth+4,_y+3)
cmbxEvtGuild_memberLogout = QtBind.createCombobox(gui_,_x,_y,_cmbxWidth,_Height)
_y+=20

# picks
_x += _cmbxWidth * 2 + 10
_y = 7
QtBind.createLabel(gui_,'Item picked up (vSRO)',_x+_cmbxWidth+4,_y+3)
cmbxEvtPick_item = QtBind.createCombobox(gui_,_x,_y,_cmbxWidth,_Height)
_y+=20
cbxEvtPick_name_filter = QtBind.createCheckBox(gui_,'cbxDoNothing','',_x,_y+3)
tbxEvtPick_name_filter = QtBind.createLineEdit(gui_,"",_x+13,_y,_tbxWidth,_Height)
_y+=20
cbxEvtPick_servername_filter = QtBind.createCheckBox(gui_,'cbxDoNothing','',_x,_y+3)
tbxEvtPick_servername_filter = QtBind.createLineEdit(gui_,"",_x+13,_y,_tbxWidth,_Height)
_y+=20
QtBind.createLabel(gui_,'Item (Rare) picked up',_x+_cmbxWidth+4,_y+3)
cmbxEvtPick_rare = QtBind.createCombobox(gui_,_x,_y,_cmbxWidth,_Height)
_y+=20
QtBind.createLabel(gui_,'Item (Equipable) picked up',_x+_cmbxWidth+4,_y+3)
cmbxEvtPick_equip = QtBind.createCombobox(gui_,_x,_y,_cmbxWidth,_Height)
_y+=20

# wrap to iterate
cmbxTriggers_={'cmbxEvtMessage_all':cmbxEvtMessage_all,'cmbxEvtMessage_private':cmbxEvtMessage_private,'cmbxEvtMessage_stall':cmbxEvtMessage_stall,'cmbxEvtMessage_party':cmbxEvtMessage_party,'cmbxEvtMessage_academy':cmbxEvtMessage_academy,'cmbxEvtMessage_guild':cmbxEvtMessage_guild,'cmbxEvtMessage_union':cmbxEvtMessage_union,'cmbxEvtMessage_global':cmbxEvtMessage_global,'cmbxEvtMessage_notice':cmbxEvtMessage_notice,'cmbxEvtMessage_gm':cmbxEvtMessage_gm,'cmbxEvtParty_joined':cmbxEvtParty_joined,'cmbxEvtParty_left':cmbxEvtParty_left,'cmbxEvtParty_memberJoin':cmbxEvtParty_memberJoin,'cmbxEvtParty_memberLeft':cmbxEvtParty_memberLeft,'cmbxEvtParty_memberLvlUp':cmbxEvtParty_memberLvlUp,'cmbxEvtGuild_noticechanged':cmbxEvtGuild_noticechanged,'cmbxEvtGuild_memberLogin':cmbxEvtGuild_memberLogin,'cmbxEvtGuild_memberLogout':cmbxEvtGuild_memberLogout,'cmbxEvtPick_item':cmbxEvtPick_item,'cmbxEvtPick_rare':cmbxEvtPick_rare,'cmbxEvtPick_equip':cmbxEvtPick_equip}

# ______________________________ Methods ______________________________ #

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

	QtBind.setChecked(gui,cbxAddTimestamp,False)
	QtBind.setChecked(gui,cbxDiscord_interactions,False)
	QtBind.setText(gui,tbxDiscord_guild_id," Discord Server ID...")
	QtBind.setChecked(gui,cbxDiscord_check_all,False)

	QtBind.setText(gui,tbxToken,'')
	
	# Reset triggers
	for name,cmbx in cmbxTriggers.items():
		QtBind.clear(gui,cmbx)
		QtBind.append(gui,cmbx,"")

	QtBind.setChecked(gui,cbxEvtMessage_uniqueSpawn_filter,False)
	QtBind.setText(gui,tbxEvtMessage_uniqueSpawn_filter," Filter by name")
	QtBind.setChecked(gui,cbxEvtMessage_uniqueKilled_filter,False)
	QtBind.setText(gui,tbxEvtMessage_uniqueKilled_filter," Filter by name")

	for name,cmbx in cmbxTriggers_.items():
		QtBind.clear(gui_,cmbx)
		QtBind.append(gui_,cmbx,"")

	QtBind.setChecked(gui_,cbxEvtMessage_global_filter,False)
	QtBind.setText(gui_,tbxEvtMessage_global_filter," Filter by message")
	QtBind.setChecked(gui_,cbxEvtMessage_notice_filter,False)
	QtBind.setText(gui_,tbxEvtMessage_notice_filter," Filter by message")

	QtBind.setChecked(gui_,cbxEvtPick_name_filter,False)
	QtBind.setText(gui_,tbxEvtPick_name_filter," Filter by name")
	QtBind.setChecked(gui_,cbxEvtPick_servername_filter,False)
	QtBind.setText(gui_,tbxEvtPick_servername_filter," Filter by servername")

# Save all config
def saveConfigs():
	# Save if data has been loaded
	if isJoined():
		# Save all data
		data = {}
		data["Channels"] = QtBind.getItems(gui,lstChannels)

		data["AddTimeStamp"] = QtBind.isChecked(gui,cbxAddTimestamp)
		data["DiscordInteractions"] = QtBind.isChecked(gui,cbxDiscord_interactions)
		data["DiscordInteractionGuildID"] = QtBind.text(gui,tbxDiscord_guild_id)
		data["DiscordInteractionCheckAll"] = QtBind.isChecked(gui,cbxDiscord_check_all)

		data["Token"] = QtBind.text(gui,tbxToken)
		
		# Save triggers from tabs
		triggers = {}
		data["Triggers"] = triggers

		for name,cmbx in cmbxTriggers.items():
			triggers[name] = QtBind.text(gui,cmbx)

		triggers["cbxEvtMessage_uniqueSpawn_filter"] = QtBind.isChecked(gui,cbxEvtMessage_uniqueSpawn_filter)
		triggers["tbxEvtMessage_uniqueSpawn_filter"] = QtBind.text(gui,tbxEvtMessage_uniqueSpawn_filter)
		triggers["cbxEvtMessage_uniqueKilled_filter"] = QtBind.isChecked(gui,cbxEvtMessage_uniqueKilled_filter)
		triggers["tbxEvtMessage_uniqueKilled_filter"] = QtBind.text(gui,tbxEvtMessage_uniqueKilled_filter)

		for name,cmbx in cmbxTriggers_.items():
			triggers[name] = QtBind.text(gui_,cmbx)

		triggers["cbxEvtMessage_global_filter"] = QtBind.isChecked(gui_,cbxEvtMessage_global_filter)
		triggers["tbxEvtMessage_global_filter"] = QtBind.text(gui_,tbxEvtMessage_global_filter)
		triggers["cbxEvtMessage_notice_filter"] = QtBind.isChecked(gui_,cbxEvtMessage_notice_filter)
		triggers["tbxEvtMessage_notice_filter"] = QtBind.text(gui_,tbxEvtMessage_notice_filter)

		triggers["cbxEvtPick_name_filter"] = QtBind.isChecked(gui_,cbxEvtPick_name_filter)
		triggers["tbxEvtPick_name_filter"] = QtBind.text(gui_,tbxEvtPick_name_filter)
		triggers["cbxEvtPick_servername_filter"] = QtBind.isChecked(gui_,cbxEvtPick_servername_filter)
		triggers["tbxEvtPick_servername_filter"] = QtBind.text(gui_,tbxEvtPick_servername_filter)

		# Overrides
		with open(getConfig(),"w") as f:
			f.write(json.dumps(data, indent=4, sort_keys=True))
		log("Plugin: "+pName+" configs has been saved")

# Loads all config previously saved
def loadConfigs():
	loadDefaultConfig()
	if isJoined():

		# Connection status
		global isOnline
		isOnline = True

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

			if "AddTimeStamp" in data and data["AddTimeStamp"]:
				QtBind.setChecked(gui,cbxAddTimestamp,True)
			if "DiscordInteractions" in data and data["DiscordInteractions"]:
				QtBind.setChecked(gui,cbxDiscord_interactions,True)
			if "DiscordInteractionGuildID" in data and data["DiscordInteractionGuildID"]:
				QtBind.setText(gui,tbxDiscord_guild_id,data["DiscordInteractionGuildID"])
			if "DiscordInteractionCheckAll" in data and data["DiscordInteractionCheckAll"]:
				QtBind.setChecked(gui,cbxDiscord_check_all,True)

			if "Token" in data:
				QtBind.setText(gui,tbxToken,data["Token"])

			# Load triggers
			if "Triggers" in data:
				triggers = data["Triggers"]

				if "cmbxEvtChar_joined" in triggers:
					QtBind.setText(gui,cmbxEvtChar_joined,triggers["cmbxEvtChar_joined"])
				if "cmbxEvtChar_disconnected" in triggers:
					QtBind.setText(gui,cmbxEvtChar_disconnected,triggers["cmbxEvtChar_disconnected"])

				if "cmbxEvtMessage_uniqueSpawn" in triggers:
					QtBind.setText(gui,cmbxEvtMessage_uniqueSpawn,triggers["cmbxEvtMessage_uniqueSpawn"])
				if "cbxEvtMessage_uniqueSpawn_filter" in triggers and triggers["cbxEvtMessage_uniqueSpawn_filter"]:
					QtBind.setChecked(gui,cbxEvtMessage_uniqueSpawn_filter,True)
				if "tbxEvtMessage_uniqueSpawn_filter" in triggers and triggers["tbxEvtMessage_uniqueSpawn_filter"]:
					QtBind.setText(gui,tbxEvtMessage_uniqueSpawn_filter,triggers["tbxEvtMessage_uniqueSpawn_filter"])
				if "cmbxEvtMessage_uniqueKilled" in triggers:
					QtBind.setText(gui,cmbxEvtMessage_uniqueKilled,triggers["cmbxEvtMessage_uniqueKilled"])
				if "cbxEvtMessage_uniqueKilled_filter" in triggers and triggers["cbxEvtMessage_uniqueKilled_filter"]:
					QtBind.setChecked(gui,cbxEvtMessage_uniqueKilled_filter,True)
				if "tbxEvtMessage_uniqueKilled_filter" in triggers and triggers["tbxEvtMessage_uniqueKilled_filter"]:
					QtBind.setText(gui,tbxEvtMessage_uniqueKilled_filter,triggers["tbxEvtMessage_uniqueKilled_filter"])

				if "cmbxEvtMessage_battlearena" in triggers:
					QtBind.setText(gui,cmbxEvtMessage_battlearena,triggers["cmbxEvtMessage_battlearena"])
				if "cmbxEvtMessage_ctf" in triggers:
					QtBind.setText(gui,cmbxEvtMessage_ctf,triggers["cmbxEvtMessage_ctf"])
				if "cmbxEvtMessage_fortress" in triggers:
					QtBind.setText(gui,cmbxEvtMessage_fortress,triggers["cmbxEvtMessage_fortress"])
				if "cmbxEvtMessage_consignmenthunter" in triggers:
					QtBind.setText(gui,cmbxEvtMessage_consignmenthunter,triggers["cmbxEvtMessage_consignmenthunter"])
				if "cmbxEvtMessage_consignmentthief" in triggers:
					QtBind.setText(gui,cmbxEvtMessage_consignmentthief,triggers["cmbxEvtMessage_consignmentthief"])

				if "cmbxEvtNear_gm" in triggers:
					QtBind.setText(gui,cmbxEvtNear_gm,triggers["cmbxEvtNear_gm"])
				if "cmbxEvtNear_unique" in triggers:
					QtBind.setText(gui,cmbxEvtNear_unique,triggers["cmbxEvtNear_unique"])
				if "cmbxEvtNear_hunter" in triggers:
					QtBind.setText(gui,cmbxEvtNear_hunter,triggers["cmbxEvtNear_hunter"])
				if "cmbxEvtNear_thief" in triggers:
					QtBind.setText(gui,cmbxEvtNear_thief,triggers["cmbxEvtNear_thief"])
				if "cmbxEvtChar_attacked" in triggers:
					QtBind.setText(gui,cmbxEvtChar_attacked,triggers["cmbxEvtChar_attacked"])
				if "cmbxEvtChar_died" in triggers:
					QtBind.setText(gui,cmbxEvtChar_died,triggers["cmbxEvtChar_died"])
				if "cmbxEvtPet_died" in triggers:
					QtBind.setText(gui,cmbxEvtPet_died,triggers["cmbxEvtPet_died"])

				if "cmbxEvtMessage_quest" in triggers:
					QtBind.setText(gui,cmbxEvtMessage_quest,triggers["cmbxEvtMessage_quest"])
				if "cmbxEvtBot_alchemy" in triggers:
					QtBind.setText(gui,cmbxEvtBot_alchemy,triggers["cmbxEvtBot_alchemy"])
				if "cmbxEvtMessage_item_sold" in triggers:
					QtBind.setText(gui,cmbxEvtMessage_item_sold,triggers["cmbxEvtMessage_item_sold"])

				# (+)
				if "cmbxEvtMessage_all" in triggers:
					QtBind.setText(gui_,cmbxEvtMessage_all,triggers["cmbxEvtMessage_all"])
				if "cmbxEvtMessage_private" in triggers:
					QtBind.setText(gui_,cmbxEvtMessage_private,triggers["cmbxEvtMessage_private"])
				if "cmbxEvtMessage_stall" in triggers:
					QtBind.setText(gui_,cmbxEvtMessage_stall,triggers["cmbxEvtMessage_stall"])
				if "cmbxEvtMessage_party" in triggers:
					QtBind.setText(gui_,cmbxEvtMessage_party,triggers["cmbxEvtMessage_party"])
				if "cmbxEvtMessage_academy" in triggers:
					QtBind.setText(gui_,cmbxEvtMessage_academy,triggers["cmbxEvtMessage_academy"])
				if "cmbxEvtMessage_guild" in triggers:
					QtBind.setText(gui_,cmbxEvtMessage_guild,triggers["cmbxEvtMessage_guild"])
				if "cmbxEvtMessage_union" in triggers:
					QtBind.setText(gui_,cmbxEvtMessage_union,triggers["cmbxEvtMessage_union"])
				if "cmbxEvtMessage_global" in triggers:
					QtBind.setText(gui_,cmbxEvtMessage_global,triggers["cmbxEvtMessage_global"])
				if "cbxEvtMessage_global_filter" in triggers and triggers["cbxEvtMessage_global_filter"]:
					QtBind.setChecked(gui_,cbxEvtMessage_global_filter,True)
				if "tbxEvtMessage_global_filter" in triggers and triggers["tbxEvtMessage_global_filter"]:
					QtBind.setText(gui_,tbxEvtMessage_global_filter,triggers["tbxEvtMessage_global_filter"])
				if "cmbxEvtMessage_notice" in triggers:
					QtBind.setText(gui_,cmbxEvtMessage_notice,triggers["cmbxEvtMessage_notice"])
				if "cbxEvtMessage_notice_filter" in triggers and triggers["cbxEvtMessage_notice_filter"]:
					QtBind.setChecked(gui_,cbxEvtMessage_notice_filter,True)
				if "tbxEvtMessage_notice_filter" in triggers and triggers["tbxEvtMessage_notice_filter"]:
					QtBind.setText(gui_,tbxEvtMessage_notice_filter,triggers["tbxEvtMessage_notice_filter"])
				if "cmbxEvtMessage_gm" in triggers:
					QtBind.setText(gui_,cmbxEvtMessage_gm,triggers["cmbxEvtMessage_gm"])

				if "cmbxEvtParty_joined" in triggers:
					QtBind.setText(gui_,cmbxEvtParty_joined,triggers["cmbxEvtParty_joined"])
				if "cmbxEvtParty_left" in triggers:
					QtBind.setText(gui_,cmbxEvtParty_left,triggers["cmbxEvtParty_left"])
				if "cmbxEvtParty_memberJoin" in triggers:
					QtBind.setText(gui_,cmbxEvtParty_memberJoin,triggers["cmbxEvtParty_memberJoin"])
				if "cmbxEvtParty_memberLeft" in triggers:
					QtBind.setText(gui_,cmbxEvtParty_memberLeft,triggers["cmbxEvtParty_memberLeft"])
				if "cmbxEvtParty_memberLvlUp" in triggers:
					QtBind.setText(gui_,cmbxEvtParty_memberLvlUp,triggers["cmbxEvtParty_memberLvlUp"])

				if "cmbxEvtGuild_noticechanged" in triggers:
					QtBind.setText(gui_,cmbxEvtGuild_noticechanged,triggers["cmbxEvtGuild_noticechanged"])
				if "cmbxEvtGuild_memberLogin" in triggers:
					QtBind.setText(gui_,cmbxEvtGuild_memberLogin,triggers["cmbxEvtGuild_memberLogin"])
				if "cmbxEvtGuild_memberLogout" in triggers:
					QtBind.setText(gui_,cmbxEvtGuild_memberLogout,triggers["cmbxEvtGuild_memberLogout"])

				if "cmbxEvtPick_item" in triggers:
					QtBind.setText(gui_,cmbxEvtPick_item,triggers["cmbxEvtPick_item"])
				if "cbxEvtPick_name_filter" in triggers and triggers["cbxEvtPick_name_filter"]:
					QtBind.setChecked(gui_,cbxEvtPick_name_filter,True)
				if "tbxEvtPick_name_filter" in triggers and triggers["tbxEvtPick_name_filter"]:
					QtBind.setText(gui_,tbxEvtPick_name_filter,triggers["tbxEvtPick_name_filter"])
				if "cbxEvtPick_servername_filter" in triggers and triggers["cbxEvtPick_servername_filter"]:
					QtBind.setChecked(gui_,cbxEvtPick_servername_filter,True)
				if "tbxEvtPick_servername_filter" in triggers and triggers["tbxEvtPick_servername_filter"]:
					QtBind.setText(gui_,tbxEvtPick_servername_filter,triggers["tbxEvtPick_servername_filter"])
				if "cmbxEvtPick_rare" in triggers:
					QtBind.setText(gui_,cmbxEvtPick_rare,triggers["cmbxEvtPick_rare"])
				if "cmbxEvtPick_equip" in triggers:
					QtBind.setText(gui_,cmbxEvtPick_equip,triggers["cmbxEvtPick_equip"])

# Return True if the text exist at the array
def ListContains(list,text):
	text = text.lower()
	for i in range(len(list)):
		if list[i].lower() == text:
			return True
	return False

# Add discord channel
def btnAddChannel_clicked():
	if character_data:
		channel_id = QtBind.text(gui,tbxChannels)
		if not channel_id:
			return
		# Check only for numbers
		if channel_id.isnumeric():
			# channel it's not empty and not added
			if not ListContains(QtBind.getItems(gui,lstChannels),channel_id):
				# Add new channel on everything
				QtBind.append(gui,lstChannels,channel_id)
				for name,cmbx in cmbxTriggers.items():
					QtBind.append(gui,cmbx,channel_id)
				for name,cmbx in cmbxTriggers_.items():
					QtBind.append(gui_,cmbx,channel_id)
				# Clear textbox to indicate success
				QtBind.setText(gui,tbxChannels,"")
				log('Plugin: Channel added ['+channel_id+']')
		else:
			log('Plugin: Error, the Discord Channel ID must be a number!')

# Remove discord channel
def btnRemChannel_clicked():
	if character_data:
		channelItem = QtBind.text(gui,lstChannels)
		# if the list has something selected
		if channelItem:
			# Remove channel from all comboboxes 
			# and leave it as default if is necessary
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
			# Remove from list
			QtBind.remove(gui,lstChannels,channelItem)
			log('Plugin: Channel removed ['+channelItem+']')

# Create an info package to send through notify
def CreateInfo(t,data):
	info = {}
	info["type"] = t
	info["data"] = data
	info["source"] = 'phBot'
	return info

# Send a notification to discord channel
# channel_id : ID from channel to be sent
# message : Text shown as discord notification
# info : Extra data used at server for some notifications
def Notify(channel_id,message,info=None,colour=None):
	# Run this in another thread to avoid locking the client/bot and wait more time for the response
	Timer(0.001,_Notify,(channel_id,message,info,colour)).start()

# Send a notification to discord channel
def _Notify(channel_id,message,info,colour):
	# Check if there is enough data to create a notification
	if not channel_id or not message:
		return
	url = URL_HOST
	if not url:
		return
	token = QtBind.text(gui,tbxToken)
	# Try to send notification
	try:
		# Add timestamp
		if QtBind.isChecked(gui,cbxAddTimestamp):
			message = "||"+datetime.now().strftime('%H:%M:%S')+"|| "+message
		# Create json to send
		data = {"token":token,"channel":channel_id,"message":message}
		if info:
			data['info'] = info
		if colour != None:
			data['colour'] = colour
		# Prepare data to send through POST method
		data = json.dumps(data).encode()
		if not url.endswith("/"):
			url += "/"
		req = urllib.request.Request(url+"api/notify",data=data,headers={'content-type':'application/json'})
		with urllib.request.urlopen(req,timeout=URL_REQUEST_TIMEOUT) as f:
			try:
				resp = json.loads(f.read().decode())
				if resp:
					if resp['success']:
						log("Plugin: Notification sent to Discord!")
					else:
						log("Plugin: Notification failed ["+resp['message']+"]")
			except Exception as ex2:
				log("Plugin: Error reading response from server ["+str(ex2)+"]")
	except Exception as ex:
		log("Plugin: Error loading url ["+str(ex)+"] to Notify")

# Fetch messages on discord (queue) from the guild server indicated
def Fetch(guild_id):
	# Run this in another thread to avoid locking the client/bot and wait more time for the response
	Timer(0.001,_Fetch,(guild_id,)).start()

# Fetch messages on discord (queue) from the guild server indicated
def _Fetch(guild_id):
	# Check if there is enough data to fetch
	if not guild_id or not guild_id.isnumeric():
		return
	url = URL_HOST
	if not url:
		return
	token = QtBind.text(gui,tbxToken)
	# Try to fetch messages
	try:
		# Prepare json to send through POST method
		params = json.dumps({'guild':guild_id,'token':token,'charname':character_data['name'],'fetch_all':QtBind.isChecked(gui,cbxDiscord_check_all)}).encode()
		if not url.endswith("/"):
			url += "/"
		req = urllib.request.Request(url+"api/fetch",data=params,headers={'content-type': 'application/json'})
		with urllib.request.urlopen(req,timeout=URL_REQUEST_TIMEOUT) as f:
			try:
				resp = json.loads(f.read().decode())
				if resp:
					if resp['success']:
						on_discord_fetch(resp['data'])
					else:
						log("Plugin: Fetch failed ["+resp['message']+"]")
			except Exception as ex2:
				log("Plugin: Error reading response from server ["+str(ex2)+"]")
	except Exception as ex:
		log("Plugin: Error loading url ["+str(ex)+"] to Fetch")

# Check if character is ingame
def isJoined():
	global character_data
	character_data = get_character_data()
	if not (character_data and "name" in character_data and character_data["name"]):
		character_data = None
	return character_data

# Get battle arena text by type
def getBattleArenaText(t):
	if t == 0:
		return 'Random'
	if t == 1:
		return 'Party'
	if t == 2:
		return 'Guild'
	if t == 3:
		return 'Job'
	return 'Unknown['+str(t)+']'

# Get Fortress text by id
def getFortressText(code):
	if code == 1:
		return "Jangan"
	if code == 3:
		return "Hotan"
	if code == 6:
		return "Bandit"
	return 'Fortress #'+str(code)

# Get the party list as discord formatted text
def getPartyTextList(party):
	if not party:
		return ''
	txt = '```\n'
	for joinId, member in party.items():
		# name + padding
		txt += member['name'].ljust(13)
		# lvl. + padding
		txt += (' (Lvl.'+str(member['level'])+')').ljust(10)
		# guild name
		if member['guild']:
			txt += ' ['+member['guild']+']'
		txt += '\n'
	txt += '```'
	return txt

# Get the guild list as discord formatted text
def getGuildTextList(guild):
	if not guild:
		return ''
	txt = '```\n'
	for memberID, member in guild.items():
		# name + padding
		txt += member['name'].ljust(13)
		# lvl. + padding
		txt += (' (Lvl.'+str(member['level'])+')').ljust(10)
		# online
		if member['online']:
			txt += ' - [On]'
		else:
			txt += ' - [Off]'
		txt += '\n'
	txt += '```'
	return txt

# Returns the current gold as text
def getGoldText():
	global character_data
	character_data = get_character_data()
	return "{:,}".format(character_data['gold'])

# Return the race type as text, empty if cannot be found
def getRaceText(servername):
	if '_CH_' in servername:
		return '(CH)'
	if '_EU_' in servername:
		return '(EU)'
	return ''

# Return the genre type as text, empty if cannot be found
def getGenreText(servername):
	if '_M_' in servername:
		return '[M]'
	if '_W_' in servername:
		return '[F]'
	return ''

# Return the sox type as text, empty if none is found
def getSoXText(servername,level):
	if level < 101:
		if servername.endswith('A_RARE'):
			return '^Star'
		elif servername.endswith('B_RARE'):
			return '^Moon'
		elif servername.endswith('C_RARE'):
			return '^Sun'
	else:
		if servername.endswith('A_RARE'):
			return '^Nova'
		elif servername.endswith('B_RARE'):
			return '^Rare'
		elif servername.endswith('C_RARE'):
			return '^Legend'
		elif servername.endswith('SET_A'):
			return '^Egy A'
		elif servername.endswith('SET_B'):
			return '^Egy B'
	return ''

# Returns the town name from consignment id
def getConsignmentTownText(code):
	if code == 0:
		return 'Jangan'
	if code == 1:
		return 'Donwhang'
	return 'Town #'+str(code)

# Loads all plugins handling chat 
def GetChatHandlers():
	import importlib
	handlers = []
	# scan files around
	plugin_name = os.path.basename(__file__)
	plugin_dir = os.path.dirname(__file__)
	for path in os.scandir(plugin_dir):
		# check python files except me
		if path.is_file() and path.name.endswith(".py") and path.name != plugin_name:
			try:
				plugin = importlib.import_module(path.name[:-3])
				# check if has chat handler
				if hasattr(plugin,'handle_chat'):
					handlers.append(getattr(plugin,'handle_chat'))
					log('Plugin: Loaded discord handler from '+path.name)
			except Exception as ex:
				log('Plugin: Error loading '+path.name+' plugin. '+str(ex))
	return handlers

# Analyze and extract item information from the index given
def ParseItem(data,index):
	rentID = struct.unpack_from('<I', data, index)[0]
	index += 4 # Rent id
	# TO DO: Parse rentability stuffs
	index += 4 # UnkUInt01
	itemID = struct.unpack_from('<I', data, index)[0]
	index += 4 # Item ID
	itemData = get_item(itemID)
	# IsEquipable
	if itemData['tid1'] == 1:
		index += 1 # plus
		index += 8 # stats
		index += 4 # durability
		count = data[index]
		index += 1 # magic options
		for i in range(count):
			index += 4 # id
			index += 4 # value
		index += 1 # (1)
		count = data[index]
		index += 1 # sockets
		for i in range(count):
			index += 1 # slot
			index += 4 # id
			index += 4 # value
		index += 1 # (2)
		count = data[index]
		index += 1 # adv
		for i in range(count):
			index += 1 # slot
			index += 4 # id
			index += 4 # value
		index += 4 # UnkUint02
	# IsCOS
	elif itemData['tid1'] == 2:
		# IsPet
		if itemData['tid2'] == 1:
			state = data[index]
			index += 1 # state
			if state != 1:
				index += 4 # model
				index += 2 + struct.unpack_from('<H', data, index)[0] # name
				# NeedsTime
				if data['tid3'] == 2:
					index += 4 # endtime
				index += 1 # UnkByte01
		# IsTransform
		elif itemData['tid2'] == 2:
			index += 4 # model
		# IsCube?
		elif itemData['tid2'] == 3:
			index += 4 # quantity
	# IsETC
	elif itemData['tid1'] == 3:
		index += 2 # quantity
		# IsAlchemy
		if itemData['tid2'] == 11:
			# IsStone
			if itemData['tid3'] == 1 or itemData['tid3'] == 2:
				index += 1 # assimilation
		# IsCard
		elif itemData['tid2'] == 14 and itemData['tid3'] == 2:
			count = data[index]
			index += 1 # params
			for i in range(count):
				index += 4 # id
				index += 4 # value
	return index,itemData

# ______________________________ Events ______________________________ #

# Scripting support to send notifications like "JellyDix,Channel ID,Message"
# Usage example "JellyDix,010010000110100100100001,This is a script notification"
def JellyDix(args):
	if len(args) >= 3:
		Notify(args[1],"|`"+character_data['name']+"`| - "+args[2])
	return 0

# Called when the character enters the game world
def joined_game():
	loadConfigs()
	Notify(QtBind.text(gui,cmbxEvtChar_joined),"|`"+character_data['name']+"`| - Joined to the game")

# Called when the character has been disconnected
def disconnected():
	global isOnline
	if isOnline:
		isOnline = False
		channel_id = QtBind.text(gui,cmbxEvtChar_disconnected)
		if channel_id:
			Notify(channel_id,"|`"+character_data['name']+"`| You has been disconnected")

# All chat messages received are sent to this function
def handle_chat(t,player,msg):
	# Check if contains item linking
	itemLink = re.search('([0-9]*)',msg)
	if itemLink:
		global chat_data
		links = itemLink.groups()
		for i in range(len(links)):
			uid = int(links[i])
			if uid in chat_data:
				item = chat_data[uid]
				race = getRaceText(item['servername'])
				genre = getGenreText(item['servername'])
				sox = getSoXText(item['servername'],item['level'])
				msg = msg.replace(''+links[i]+'','`< '+item['name']+(' '+race if race else '')+(' '+genre if genre else '')+(' '+sox if sox else '')+' >`')
			else:
				msg = msg.replace(''+links[i]+'','`< '+links[i]+' >`')
	# Check message type
	if t == 1:
		Notify(QtBind.text(gui_,cmbxEvtMessage_all),"|`"+character_data['name']+"`| - [**General**] from `"+player+"`: "+msg)
	elif t == 2:
		Notify(QtBind.text(gui_,cmbxEvtMessage_private),"|`"+character_data['name']+"`| - [**Private**] from `"+player+"`: "+msg)
	elif t == 9:
		Notify(QtBind.text(gui_,cmbxEvtMessage_stall),"|`"+character_data['name']+"`| - [**Stall**] from `"+player+"`: "+msg)
	elif t == 4:
		Notify(QtBind.text(gui_,cmbxEvtMessage_party),"|`"+character_data['name']+"`| - "+"[**Party**] `"+player+"`: "+msg)
	elif t == 16:
		Notify(QtBind.text(gui_,cmbxEvtMessage_academy),"|`"+character_data['name']+"`| - "+"[**Academy**] `"+player+"`: "+msg)
	elif t == 5:
		Notify(QtBind.text(gui_,cmbxEvtMessage_guild),"[**Guild**] `"+player+"`: "+msg)
	elif t == 11:
		Notify(QtBind.text(gui_,cmbxEvtMessage_union),"[**Union**] `"+player+"`: "+msg)
	elif t == 6:
		if QtBind.isChecked(gui_,cbxEvtMessage_global_filter):
			searchMessage = QtBind.text(gui_,tbxEvtMessage_global_filter)
			if searchMessage:
				try:
					if re.search(searchMessage,msg):
						Notify(QtBind.text(gui_,cmbxEvtMessage_global),"[**Global**] `"+player+"`: "+msg,colour=0xffeb3b)
				except Exception as ex:
					log("Plugin: Error at regex ["+str(ex)+"]")
		else:
			Notify(QtBind.text(gui_,cmbxEvtMessage_global),"[**Global**] `"+player+"`: "+msg,colour=0xffeb3b)
	elif t == 7:
		if QtBind.isChecked(gui_,cbxEvtMessage_notice_filter):
			searchMessage = QtBind.text(gui_,tbxEvtMessage_notice_filter)
			if searchMessage:
				try:
					if re.search(searchMessage,msg):
						Notify(QtBind.text(gui_,cmbxEvtMessage_notice),"[**Notice**] : "+msg)
				except Exception as ex:
					log("Plugin: Error at regex ["+str(ex)+"]")
		else:
			Notify(QtBind.text(gui_,cmbxEvtMessage_notice),"[**Notice**] : "+msg)
	elif t == 3:
		Notify(QtBind.text(gui_,cmbxEvtMessage_gm),"[**GameMaster**] `"+player+"`: "+msg)

# Called for specific events. data field will always be a string.
def handle_event(t, data):
	# Filter events
	if t == 9:
		Notify(QtBind.text(gui,cmbxEvtNear_gm),"|`"+character_data['name']+"`| - **GameMaster** `"+data+"` is near to you!",CreateInfo("position",get_position()))
	elif t == 0:
		Notify(QtBind.text(gui,cmbxEvtNear_unique),"|`"+character_data['name']+"`| - **"+data+"** unique is near to you!",CreateInfo("position",get_position()))
	elif t == 1:
		Notify(QtBind.text(gui,cmbxEvtNear_hunter),"|`"+character_data['name']+"`| - **Hunter/Trader** `"+data+"` is near to you!",CreateInfo("position",get_position()))
	elif t == 2:
		Notify(QtBind.text(gui,cmbxEvtNear_thief),"|`"+character_data['name']+"`| - **Thief** `"+data+"` is near to you!",CreateInfo("position",get_position()))
	elif t == 4:
		Notify(QtBind.text(gui,cmbxEvtChar_attacked),"|`"+character_data['name']+"`| - `"+data+"` is attacking you!",colour=0xFF5722)
	elif t == 7:
		Notify(QtBind.text(gui,cmbxEvtChar_died),"|`"+character_data['name']+"`| - You died",CreateInfo("position",get_position()))
	elif t == 3:
		pet = get_pets()[data]
		Notify(QtBind.text(gui,cmbxEvtPet_died),"|`"+character_data['name']+"`| - Your pet `"+(pet['type'].title())+"` died")
	elif t == 5:
		channel_id = QtBind.text(gui_,cmbxEvtPick_rare)
		if channel_id:
			item = get_item(int(data))
			race = getRaceText(item['servername'])
			genre = getGenreText(item['servername'])
			sox = getSoXText(item['servername'],item['level'])
			Notify(channel_id,"|`"+character_data['name']+"`| - **Item (Rare)** picked up ***"+item['name']+(' '+race if race else '')+(' '+genre if genre else '')+(' '+sox if sox else '')+"***")
	elif t == 6:
		channel_id = QtBind.text(gui_,cmbxEvtPick_equip)
		if channel_id:
			item = get_item(int(data))
			race = getRaceText(item['servername'])
			genre = getGenreText(item['servername'])
			sox = getSoXText(item['servername'],item['level'])
			Notify(channel_id,"|`"+character_data['name']+"`| - **Item (Equipable)** picked up ***"+item['name']+(' '+race if race else '')+(' '+genre if genre else '')+(' '+sox if sox else '')+"***")
	elif t == 8:
		Notify(QtBind.text(gui,cmbxEvtBot_alchemy),"|`"+character_data['name']+"`| - **Auto alchemy** has been completed")

# All packets received from game server will be passed to this function
# Returning True will keep the packet and False will not forward it to the game client
def handle_joymax(opcode, data):
	# globals used in more than one IF statement
	global party_data,hasStall

	# SERVER_NOTICE_UPDATE
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
								Notify(channel_id,"**"+uniqueName+"** has appeared",colour=0x9C27B0)
						except Exception as ex:
							log("Plugin: Error at regex ["+str(ex)+"]")
				else:
					Notify(channel_id,"**"+uniqueName+"** has appeared",colour=0x9C27B0)
		elif updateType == 6:
			channel_id = QtBind.text(gui,cmbxEvtMessage_uniqueKilled)
			if channel_id:
				modelID = struct.unpack_from("<I",data,2)[0]
				killerNameLength = struct.unpack_from('<H', data, 6)[0]
				killerName = struct.unpack_from('<' + str(killerNameLength) + 's', data, 8)[0].decode('cp1252')
				uniqueName = get_monster(int(modelID))['name']
				if QtBind.isChecked(gui,cbxEvtMessage_uniqueKilled_filter):
					searchName = QtBind.text(gui,tbxEvtMessage_uniqueKilled_filter)
					if searchName:
						try:
							if re.search(searchName,uniqueName):
								Notify(channel_id,"**"+uniqueName+"** killed by `"+killerName+"`",colour=0x9C27B0)
						except Exception as ex:
							log("Plugin: Error at regex ["+str(ex)+"]")
				else:
					Notify(channel_id,"**"+uniqueName+"** killed by `"+killerName+"`",colour=0x9C27B0)
		elif updateType == 29:
			jobType = data[2]
			if jobType == 1:
				channel_id = QtBind.text(gui,cmbxEvtMessage_consignmenthunter)
				if channel_id:
					progressType = data[3]
					if progressType == 0:
						Notify(channel_id,"[**Consignment**] Hunter trade will start at 10 minutes")
					elif progressType == 1:
						Notify(channel_id,"[**Consignment**] Hunter trade started ("+getConsignmentTownText(data[4])+")")
					elif progressType == 2:
						Notify(channel_id,"[**Consignment**] Hunter trade has ended")
			elif jobType == 2:
				channel_id = QtBind.text(gui,cmbxEvtMessage_consignmentthief)
				if channel_id:
					progressType = data[3]
					if progressType == 0:
						Notify(channel_id,"[**Consignment**] Thief trade will start at 10 minutes")
					elif progressType == 1:
						Notify(channel_id,"[**Consignment**] Thief trade started ("+getConsignmentTownText(data[4])+")")
					elif progressType == 2:
						Notify(channel_id,"[**Consignment**] Thief trade has ended")
	# SERVER_BA_NOTICE
	elif opcode == 0x34D2:
		channel_id = QtBind.text(gui,cmbxEvtMessage_battlearena)
		if channel_id:
			updateType = data[0]
			if updateType == 2:
				Notify(channel_id,"[**Battle Arena**] ("+getBattleArenaText(data[1])+") will start at 10 minutes")
			elif updateType == 13:
				Notify(channel_id,"[**Battle Arena**] ("+getBattleArenaText(data[1])+") will start at 5 minutes")
			elif updateType == 14:
				Notify(channel_id,"[**Battle Arena**] ("+getBattleArenaText(data[1])+") will start at 1 minute")
			elif updateType == 3:
				Notify(channel_id,"[**Battle Arena**] registration period has ended")
			elif updateType == 4:
				Notify(channel_id,"[**Battle Arena**] started")
			elif updateType == 5:
				Notify(channel_id,"[**Battle Arena**] has ended")
	# SERVER_CTF_NOTICE
	elif opcode == 0x34B1:
		channel_id = QtBind.text(gui,cmbxEvtMessage_ctf)
		if channel_id:
			updateType = data[0]
			if updateType == 2:
				Notify(channel_id,"[**Capture the Flag**] will start at 10 minutes")
			elif updateType == 13:
				Notify(channel_id,"[**Capture the Flag**] will start at 5 minutes")
			elif updateType == 14:
				Notify(channel_id,"[**Capture the Flag**] will start at 1 minute")
			elif updateType == 3:
				Notify(channel_id,"[**Capture the Flag**] started")
			elif updateType == 9:
				Notify(channel_id,"[**Capture the Flag**] has ended")
	# SERVER_QUEST_UPDATE
	elif opcode == 0x30D5:
		channel_id = QtBind.text(gui,cmbxEvtMessage_quest)
		if channel_id:
			# Quest update & Quest completed
			if data[0] == 2 and data[10] == 2:
				questID = struct.unpack_from("<I",data,1)[0]
				quest = get_quests()[questID]
				Notify(channel_id,"|`"+character_data['name']+"`| - **Quest** has been completed ***"+quest['name']+"***")
	# SERVER_INVENTORY_ITEM_MOVEMENT
	elif opcode == 0xB034:
		# vSRO filter
		locale = get_locale()
		if locale == 22:
			channel_id = QtBind.text(gui_,cmbxEvtPick_item)
			if channel_id:
				# parse
				updateType = data[1]
				if updateType == 6: # Ground
					notify_pickup(channel_id,struct.unpack_from("<I",data,7)[0])
				elif updateType == 17: # Pet
					notify_pickup(channel_id,struct.unpack_from("<I",data,11)[0])
				elif updateType == 28: # Pet (Full/Quest)
					slotInventory = data[6]
					if slotInventory != 254:
						notify_pickup(channel_id,struct.unpack_from("<I",data,11)[0])
	# SERVER_FW_NOTICE
	elif opcode == 0x385F:
		channel_id = QtBind.text(gui,cmbxEvtMessage_fortress)
		if channel_id:
			updateType = data[0]
			if updateType == 1:
				Notify(channel_id,"[**Fortress War**] will start in 30 minutes")
			elif updateType == 2:
				Notify(channel_id,"[**Fortress War**] started")
			elif updateType == 3:
				Notify(channel_id,"[**Fortress War**] has 30 minutes before the end")
			elif updateType == 4:
				Notify(channel_id,"[**Fortress War**] has 20 minutes before the end")
			elif updateType == 5:
				Notify(channel_id,"[**Fortress War**] has 10 minutes before the end")
			elif updateType == 8:
				fortressID = struct.unpack_from("<I",data,1)[0]
				guildNameLength = struct.unpack_from("<H",data,5)[0]
				guildName = data[7:7+guildNameLength].decode('cp1252')
				Notify(channel_id,"[**Fortress War**] "+getFortressText(fortressID)+" has been taken by `"+guildName+"`")
			elif updateType == 9:
				Notify(channel_id,"[**Fortress War**] has 1 minute before the end")
			elif updateType == 6:
				Notify(channel_id,"[**Fortress War**] has ended")
	# SERVER_PARTY_DATA
	elif opcode == 0x3065:
		party_data = get_party()
		channel_id = QtBind.text(gui_,cmbxEvtParty_joined)
		if channel_id:
			Notify(channel_id,"|`"+character_data['name']+"`| You has been joined to the party\n"+getPartyTextList(party_data))
	# SERVER_PARTY_UPDATE
	elif opcode == 0x3864:
		updateType = data[0]
		if updateType == 1:
			Notify(QtBind.text(gui_,cmbxEvtParty_left),"|`"+character_data['name']+"`| You left the party!")
		elif updateType == 2:
			party_data = get_party()
			channel_id = QtBind.text(gui_,cmbxEvtParty_memberJoin)
			if channel_id:
				memberNameLength = struct.unpack_from('<H',data,6)[0]
				memberName = struct.unpack_from('<'+str(memberNameLength)+'s',data,8)[0].decode('cp1252')
				Notify(channel_id,"|`"+character_data['name']+"`| `"+memberName+"` joined to the party\n"+getPartyTextList(party_data))
		elif updateType == 3:
			joinID = struct.unpack_from("<I",data,1)[0]
			memberName = party_data[joinID]['name']
			party_data = get_party()
			if memberName == character_data['name']:
				Notify(QtBind.text(gui_,cmbxEvtParty_left),"|`"+character_data['name']+"`| You left the party")
			else:
				channel_id = QtBind.text(gui_,cmbxEvtParty_memberLeft)
				if channel_id:
					Notify(channel_id,"|`"+character_data['name']+"`| `"+memberName+"` left the party\n"+getPartyTextList(party_data))
		elif updateType == 6: # update member
			if data[5] == 2: # level
				channel_id = QtBind.text(gui_,cmbxEvtParty_memberLvlUp)
				if channel_id:
					joinID = struct.unpack_from("<I",data,1)[0]
					newLevel = data[6]
					oldLevel = party_data[joinID]['level']
					party_data[joinID]['level'] = newLevel
					if oldLevel < newLevel:
						Notify(channel_id,"|`"+character_data['name']+"`| `"+party_data[joinID]['name']+"` level up!\n"+getPartyTextList(party_data))
	# SERVER_STALL_CREATE_RESPONSE
	elif opcode == 0xB0B1:
		if data[0] == 1:
			hasStall = True
	# SERVER_STALL_DESTROY_RESPONSE
	elif opcode == 0xB0B2:
		if data[0] == 1:
			hasStall = False
	# SERVER_STALL_ENTITY_ACTION
	elif opcode == 0x30B7:
		if data[0] == 3 and hasStall:
			channel_id = QtBind.text(gui,cmbxEvtMessage_item_sold)
			if channel_id:
				playerNameLength = struct.unpack_from('<H', data, 2)[0]
				playerName = struct.unpack_from('<' + str(playerNameLength) + 's', data, 4)[0].decode('cp1252')
				Notify(channel_id,"|`"+character_data['name']+"`| `"+playerName+"` bought an item from your stall\n```Your gold now: "+getGoldText()+"```")
	# SERVER_CHAT_ITEM_DATA
	elif opcode == 0xB504:
		global chat_data
		index = 2
		for i in range(data[1]):
			uid = struct.unpack_from('<I', data, index)[0]
			index += 4 # Unique ID
			try:
				index, item = ParseItem(data,index)
				chat_data[uid] = item
			except Exception as ex:
				# Make easy log file for user
				with open(getPath()+"error.log","a") as f:
					f.write("["+str(ex)+"] Server: (Opcode) 0x" + '{:02X}'.format(opcode) + " (Data) "+ ("None" if not data else ' '.join('{:02X}'.format(x) for x in data))+'\r\n')
	# GUILD_INFO_UPDATE
	elif opcode == 0x38F5:
		updateType = data[0]
		if updateType == 6: # member update
			memberID = struct.unpack_from("<I",data,1)[0]
			infoType = data[5]
			if infoType == 2: # session
				if data[6]:
					channel_id = QtBind.text(gui_,cmbxEvtGuild_memberLogout)
					if channel_id:
						member = get_guild()[memberID]
						Notify(channel_id,"|`"+character_data['name']+"`| Guild member `"+member['name']+"` has logged off")
				else:
					channel_id = QtBind.text(gui_,cmbxEvtGuild_memberLogin)
					if channel_id:
						member = get_guild()[memberID]
						# Avoid myself
						if member['name'] != character_data['name']:
							Notify(channel_id,"|`"+character_data['name']+"`|  Guild member `"+member['name']+"` has logged on")
		elif updateType == 5: # general info
			infoType = data[1]
			if infoType == 16: # notice changed
				channel_id = QtBind.text(gui_,cmbxEvtGuild_noticechanged)
				if channel_id:
					index = 2
					titleLength = struct.unpack_from('<H', data, index)[0]
					title = struct.unpack_from('<' + str(titleLength) + 's', data,index+2)[0].decode('cp1252')
					index+=2+titleLength
					textLength = struct.unpack_from('<H', data,index)[0]
					text = struct.unpack_from('<' + str(textLength) + 's', data, index+2)[0].decode('cp1252')
					Notify(channel_id,"|`"+character_data['name']+"`| Guild notice updated : **`"+title+"`**\n"+text)
	return True

# All picked up items are sent to this function (only vSRO working at the moment) 
def notify_pickup(channel_id,itemID):
	item = get_item(itemID)
	# Check filters
	usefilterName = QtBind.isChecked(gui_,cbxEvtPick_name_filter)
	usefilterServerName = QtBind.isChecked(gui_,cbxEvtPick_servername_filter)
	if not usefilterName and not usefilterServerName:
		# No filters activated
		race = getRaceText(item['servername'])
		genre = getGenreText(item['servername'])
		sox = getSoXText(item['servername'],item['level'])
		Notify(channel_id,"|`"+character_data['name']+"`| - **Item** picked up ***"+item['name']+(' '+race if race else '')+(' '+genre if genre else '')+(' '+sox if sox else '')+"***")
		return
	# check filter name
	if usefilterName:
		searchName = QtBind.text(gui_,tbxEvtPick_name_filter)
		if searchName:
			try:
				if re.search(searchName,item['name']):
					# Filtered by Name
					race = getRaceText(item['servername'])
					genre = getGenreText(item['servername'])
					sox = getSoXText(item['servername'],item['level'])
					Notify(channel_id,"|`"+character_data['name']+"`| - **Item (Filtered)** picked up ***"+item['name']+(' '+race if race else '')+(' '+genre if genre else '')+(' '+sox if sox else '')+"***")
					return
			except Exception as ex:
				log("Plugin: Error at regex (name) ["+str(ex)+"]")
	# check filter servername
	if usefilterServerName:
		searchServername = QtBind.text(gui_,tbxEvtPick_servername_filter)
		if searchServername:
			try:
				if re.search(searchServername,item['servername']):
					# Filtered by server name
					race = getRaceText(item['servername'])
					genre = getGenreText(item['servername'])
					sox = getSoXText(item['servername'],item['level'])
					Notify(channel_id,"|`"+character_data['name']+"`| - **Item (Filtered)** picked up ***"+item['name']+(' '+race if race else '')+(' '+genre if genre else '')+(' '+sox if sox else '')+"***")
					return
			except Exception as ex:
				log("Plugin: Error at regex (servername) ["+str(ex)+"]")

# Called every 500ms
def event_loop():
	# Check if is in game at first
	if character_data:
		# generate fetch stuff
		global discord_fetch_counter
		discord_fetch_counter += 500
		# Check if delay is longer to start fetching
		if discord_fetch_counter >= DISCORD_FETCH_DELAY:
			discord_fetch_counter = 0
			if QtBind.isChecked(gui,cbxDiscord_interactions):
				# Fetch messages from guild
				Fetch(QtBind.text(gui,tbxDiscord_guild_id))

# Called everytime discord has been fetch
def on_discord_fetch(data):
	if not data:
		return
	# fetch messages date
	fetched_at = time.strptime(str(data['fetched_at']), '%m/%d/%Y, %H:%M:%S')
	fetched_at = time.mktime(fetched_at)
	# analyzing messages
	messages = data['messages']
	for message in messages:
		# created message date
		created_at = time.strptime(str(message['created_at']), '%m/%d/%Y, %H:%M:%S')
		created_at = time.mktime(created_at)
		# check if the time is shorter than 15 seconds for handling messages
		seconds_difference = int(fetched_at-created_at)
		if seconds_difference <= 15:
			# sent message through every handler
			content = message['content']
			for handler in discord_chat_handlers:
				try:
					handler(100,'',content)
				except Exception as ex:
					# fail silent
					pass
			# try to check native interaction
			on_discord_message(content,message['channel_id'])

# Called everytime a discord message is sent to bot
def on_discord_message(msg,channel_id):
	channel_id = str(channel_id)
	msgLower = msg.lower()
	if msgLower.startswith('get '):
		# remove first command
		msgLower = msgLower[4:].rstrip()
		if msgLower == 'position':
			p = get_position()
			Notify(channel_id,'|`'+character_data['name']+'`| - Your actual position is ( X:%.1f, Y:%.1f, Region:%d )'%(p['x'],p['y'],p['region']),CreateInfo('position',p))
		elif msgLower == 'party':
			party = get_party()
			if party:
				Notify(channel_id,'|`'+character_data['name']+'`| - Your party members are :\n'+getPartyTextList(party))
			else:
				Notify(channel_id,'|`'+character_data['name']+'`| - You are not in party!')
		elif msgLower == 'guild':
			guild = get_guild()
			if guild:
				Notify(channel_id,'|`'+character_data['name']+'`| - Your guild members from `'+character_data['guild']+'` are :\n'+getGuildTextList(guild))
			else:
				Notify(channel_id,'|`'+character_data['name']+'`| - You are not in a guild!')
		elif msgLower == 'exp':
			data = get_character_data()
			percentExp = data['current_exp'] * 100 / data['max_exp'] 
			Notify(channel_id,'|`'+character_data['name']+'`| - Your current exp is %.2f' % percentExp)

# Plugin loaded
log('Plugin: '+pName+' v'+pVersion+' successfully loaded')

if not os.path.exists(getPath()):
	# Creating configs folder
	os.makedirs(getPath())
	log('Plugin: '+pName+' folder has been created')
# Adding RELOAD plugin support
loadConfigs()

# Load discord handlers
discord_chat_handlers = GetChatHandlers()
