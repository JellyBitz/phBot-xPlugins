from phBot import *
from threading import Timer
from time import sleep
import sqlite3
import struct
import os

pName = 'xScriptHelper'
pVersion = '1.4.0'
pUrl = 'https://raw.githubusercontent.com/JellyBitz/phBot-xPlugins/master/xScriptHelper.py'

# Script Commands :
# - Take items from character storage but keeping the space on inventory empty
# DoStorageTakeLimit,emptySlots
# - Switch from script and restart bot to apply changes
# SwitchScript,C:\path\to\script.txt
# - Switch profile to default or any other one existing and restarts bot to apply changes
# SwitchProfile
# SwitchProfile,FasterAttack

# ______________________________ Initializing ______________________________ #

# globals
StorageData = None
CharacterData = None

# ______________________________ Methods ______________________________ #

def Inject_SelectEntity(EntityID):
	inject_joymax(0x7045,struct.pack('<I',EntityID),False)

def Inject_RequestStorageData(EntityID):
	p = struct.pack('<IB',EntityID,0)
	inject_joymax(0x703C,p,False)

def Inject_NpcTalk(EntityID,TalkID):
	p = struct.pack('<IB',EntityID,TalkID)
	inject_joymax(0x7046,p,False)

def Inject_InventoryStorageMovement(MovementType,SlotInitial,SlotFinal,EntityID):
	p = struct.pack('B',MovementType)
	p += struct.pack('B',SlotInitial)
	p += struct.pack('B',SlotFinal)
	p += struct.pack('<I',EntityID)
	inject_joymax(0x7034,p,False)

def Inject_ExitNpc(EntityID):
	inject_joymax(0x704B,struct.pack('<I',EntityID),False)

# Count slots availables on inventory
def CountInventoryEmptySlots():
	items = get_inventory()['items']
	count = 0
	# check items between intervals
	for slot, item in enumerate(items):
		if slot >= 13:
			if not item:
				count+=1
	return count

# Finds an empty slot, returns -1 if inventory is full
def GetInventoryEmptySlot():
	items = get_inventory()['items']
	# check the first empty
	for slot, item in enumerate(items):
		if slot >= 13:
			if not item:
				return slot
	return -1

# Find npc by name or servername through lambda expression and return his information
def FindNpcByExpression(_lambda):
	npcs = get_npcs()
	if npcs:
		for uid, npc in npcs.items():
			# Search by lambda
			if _lambda(npc['name'],npc['servername']):
				# Save unique id
				npc['entity_id'] = uid
				return npc
	return None

# Executes all the process to open, take items, and close storage
def DoStorageTakeLimitTask(NpcInfo,KeepInventoryEmptySlots):
	entityID = NpcInfo['entity_id']
	# Check if storage has been loaded and try to open it
	if not StorageData:
		log("Plugin: Loading Storage...")
		# Try to select NPC
		Inject_SelectEntity(entityID)
		sleep(2)
		# Load data
		Inject_RequestStorageData(entityID)
		sleep(2)
		# Close it
		Inject_ExitNpc(entityID)
		sleep(2)
	# Check if some item can be taken
	conn = GetFilterConnection()
	item = GetTakeableStorageItem(conn)
	if not item:
		# Stop looking for it
		conn.close()
		return
	# stop bot script
	stop_bot()
	sleep(1)
	# open npc to start the process again since phBot close it
	log("Plugin: Selecting NPC...")
	Inject_SelectEntity(entityID)
	sleep(2)
	log("Plugin: Entering NPC...")
	Inject_NpcTalk(entityID,3)
	sleep(2)
	# double check infinite loop
	takeCurrentSlot = 0 
	takeAttempts = 0
	takeAttemptsMax = 3
	# Try to take item
	while item:
		emptySlot = GetInventoryEmptySlot()
		if not emptySlot:
			# Inventory is full
			break
		# Track a max attempts on the next take
		takeCurrentSlot = item['slot']
		# Move item from storage to empty slot
		log('Plugin: Taking item "'+item['name']+'"...')
		Inject_InventoryStorageMovement(3,item['slot'],emptySlot,entityID)
		# Wait a little
		sleep(2)
		# Check if empty slots has been reached
		if CountInventoryEmptySlots() <= KeepInventoryEmptySlots:
			break
		# Search for another item
		item = GetTakeableStorageItem(conn)
		if not item:
			break
		# Track max attempts
		if takeCurrentSlot == item['slot']:
			takeAttempts+=1
		else:
			takeAttempts=0
		if takeAttempts == takeAttemptsMax:
			log("Plugin: Unnexpected error, too many attempts to take the item. Aborting...")
			break
	# All done
	conn.close()
	log("Plugin: Exiting NPC...")
	Inject_ExitNpc(entityID)
	sleep(1)
	# restart bot
	start_bot()

# Create a database connection to config filter
def GetFilterConnection():
	# Path to the filter database
	path = get_config_dir()+CharacterData['server']+'_'+CharacterData['name']+'.db3'
	# Connect to db3
	return sqlite3.connect(path)

# Check if character is ingame
def IsJoined():
	global CharacterData
	CharacterData = get_character_data()
	if not (CharacterData and "name" in CharacterData and CharacterData["name"]):
		CharacterData = None
	return CharacterData

# Search for an takeable item from storage by using the filter database
def GetTakeableStorageItem(FilterConnection):
	global StorageData
	StorageData = get_storage()
	if not StorageData:
		return None
	# Check all items and compare to database
	items = StorageData['items']
	c = FilterConnection.cursor()
	for slot, item in enumerate(items):
		# avoid empty slots
		if item:
			# Check if can be taken
			if c.execute('SELECT EXISTS(SELECT 1 FROM pickfilter WHERE id=? AND takestorage=1 LIMIT 1)',(item['model'],)).fetchone()[0]:
				item['slot'] = slot
				return item
	return None

# ______________________________ Events ______________________________ #

# Takes items from storage
def DoStorageTakeLimit(args):
	# check params
	keepEmptySlots = 0
	if len(args) > 1:
		keepEmptySlots = int(args[1])
	# check if there is space available
	emptySlots = CountInventoryEmptySlots()
	if emptySlots <= keepEmptySlots:
		# cancel process, no space available
		return 0
	# Check if storage is near
	npcInfo = FindNpcByExpression(lambda n,s: '_WAREHOUSE' in s)
	if npcInfo:
		# Avoid lock bot thread
		Timer(0.001,DoStorageTakeLimitTask,[npcInfo,keepEmptySlots]).start()
		# Wait a little bit while opening NPC and check items
		return 7000
	else:
		log("Plugin: Storage is not near!")
		return 0

# Change script and restart bot
def SwitchScript(args):
	if len(args) < 2:
		log('Plugin: Not enough parameters to use "SwitchScript" command')
	# Try to change script
	if os.path.exists(args[1]):
		# Stop
		stop_bot()
		# Change script
		set_training_script(args[1])
		# Restart
		Timer(0.1,start_bot).start()
	else:
		log('Plugin: Path not found ['+args[1]+']')
	return 0

# Change profile and restart bot
def SwitchProfile(args):
	# Stop it
	stop_bot()
	# Change profile
	if len(args) < 2:
		if set_profile(''):
			log('Plugin: Profile changed to Default')
		else:
			log('Plugin: Error changing profile!')
	else:
		if set_profile(args[1]):
			log('Plugin: Profile changed to ['+args[1]+']')
		else:
			log('Plugin: Error changing profile!')
	# Restart
	Timer(0.1,start_bot).start()
	return 0

# Called when the character enters the game world
def joined_game():
	global CharacterData
	CharacterData = get_character_data()

# Called after being teleported
def teleported():
	global StorageData
	StorageData = None

# All packets received from game server will be passed to this function
# Returning True will keep the packet and False will not forward it to the game client
def handle_joymax(opcode, data):
	# SERVER_ALCHEMY_DISMANTLE_RESPONSE
	if opcode == 0xB157:
		# check failure
		if data[0] != 1:
			global DismantlingErrorCode
			DismantlingErrorCode = struct.unpack_from('<H',data,1)[0]
	# SERVER_STORAGE_DATA_END
	elif opcode == 0x3048:
		global StorageData
		StorageData = get_storage()
	return True

# Plugin loaded
log('Plugin: '+pName+' v'+pVersion+' succesfully loaded')

# Check if storage has been loaded
if IsJoined():
	StorageData = get_storage()
