from phBot import *
from threading import Timer
from threading import Event
from time import sleep
import sqlite3
import json
import struct
import os

pVersion = '1.0.1'
pName = 'xBattleInfinity'
pUrl = 'https://raw.githubusercontent.com/JellyBitz/phBot-xPlugins/master/xBattleInfinity.py'

# ______________________________ Initializing ______________________________ #

# Globals
character_data = get_character_data()
SelectedUID = 0
EventObjectSelected = Event()
EventItemPickup = Event()
EventTeleported = Event()
InfinityPartyMode = False
InfinityMaskMode = 'A'
InfinityActivated = False
InfinityMaskEnabled = False

# ______________________________ Methods ______________________________ #

# Calc the distance from point A to B
def GetDistance(ax,ay,bx,by):
	return ((bx-ax)**2 + (by-ay)**2)**(0.5)

# Create a database connection to config filter
def GetFilterConnection():
	# Path to the filter database
	path = get_config_dir()+character_data['server']+'_'+character_data['name']+'.db3'
	# Connect to db3
	return sqlite3.connect(path)

def IsPickable(filterCursor,ItemID):
	# Check existence of pickable item by character
	return filterCursor.execute('SELECT EXISTS(SELECT 1 FROM pickfilter WHERE id=? AND pick=1 LIMIT 1)',(ItemID,)).fetchone()[0]

# Create a connection to database
def GetDatabaseConnection():
	bot_path = os.getcwd()
	# Load the server info
	data = {}
	locale = get_locale()
	# vSRO
	if locale == 22:
		with open(bot_path+"/vSRO.json","r") as f:
			data = json.load(f)
		# Match data with the current server name
		server = character_data['server']
		for k in data:
			servers = data[k]['servers']
			# Check if servers is in list
			if server in servers:
				# Scan data folder
				for path in os.scandir(bot_path+"/Data"):
					# Check databases only
					if path.is_file() and path.name.endswith(".db3"):
						# Connect to check if the data matches
						conn = sqlite3.connect(bot_path+"/Data/"+path.name)
						c = conn.cursor()
						c.execute('SELECT * FROM data WHERE k="path" AND v=?',(data[k]['path'],))
						if c.fetchone():
							# match found
							return conn
						else:
							conn.close()
	# TrSRO
	elif locale == 56:
		conn = sqlite3.connect(bot_path+"/Data/TRSRO.db3")
		return conn
	return None

# Returns the info from the skill id given or None
def GetSkillByID(ID):
	conn = GetDatabaseConnection()
	row = conn.cursor().execute('SELECT * FROM skills WHERE id=?',(ID,)).fetchone()
	result = {}
	if row:
		result['id'] = row[0]
		result['servername'] = row[2]
		result['name'] = row[3]
		result['cast_time'] = row[4]
		result['cool_down'] = row[5]
		result['duration'] = row[6]
	conn.close()
	return result

# Extract all info from arguments
def LoadSkills(Skills):
	skills = {}
	for skillID in Skills:
		# Load skill data
		skillData = GetSkillByID(skillID)
		# Check existence
		if not skillData:
			log('Plugin: Skill (#'+str(skillID)+') not found')
			continue
		# Check if is attacking skill
		if not skillData['duration'] == 0:
			log('Plugin: Skill (#'+str(skillID)+') is not an attacking skill!')
			continue
		# Add variable to control activation cooldown
		skillData['ready'] = True

		skills[skillID] = skillData
	return skills

# Returns the first monster around or None
def FindMonster(Position,Radius):
	monsters = get_monsters()
	if monsters:
		# Return the first one inside radius
		for uid, monster in monsters.items():
			if round(GetDistance(Position['x'],Position['y'],monster['x'],monster['y']),2) <= Radius:
				monster['uid'] = uid
				return monster
	return None

# Returns the first skill ready to be used or None
def FindReadySkill(Skills):
	for n in Skills:
		skill = Skills[n]
		if skill['ready']:
			return skill
	return None

# Moves the character to the coordinate position, returns activation
def MoveToPosition(Position):
	position = get_position()
	# Check if is more than 3m from distance to the given position
	if GetDistance(position['x'],position['y'],Position['x'],Position['y']) > 3:
		move_to(Position['x'],Position['y'],Position['z'])
		return True
	return False

# Attack all mobs around
def AttackInfinityTask(Position,Radius,Skills,Timeout):
	# Used to pass and modify values through arguments
	task = {}
	task['IsRunning'] = True
	# Stops this task
	def TimeoutTask(Task):
		# No mobs around, attacking process over
		log("Plugin: No monsters around for a long time!")
		Task['IsRunning'] = False
	# Timer acting as timeout to stop the task when there is no mobs around
	timerTimeout = None
	# Declare quick access
	global SelectedUID
	# Start process to kill mobs
	while task['IsRunning']:

		# Set skill for attacking
		skill = FindReadySkill(Skills)
		if not skill:
			# All skills are in cooldown
			sleep(0.05)
			continue

		# Find some mob to attack
		mob = FindMonster(Position,Radius)
		if not mob:
			# Start timeout timer from mobs
			if not timerTimeout:
				timerTimeout = Timer(Timeout,TimeoutTask,[task])
				timerTimeout.start()
				log("Plugin: No monsters around, waiting...")
			# Goes back to center
			MoveToPosition(Position)
			sleep(1)
			continue
		# Check if is running
		if timerTimeout:
			timerTimeout.cancel()
			timerTimeout = None
		
		# Try select mob as target
		selectingAttempts = 0
		selectingAttemptsMax = 3
		findAnotherMob = False
		while SelectedUID != mob['uid']:
			if selectingAttempts >= selectingAttemptsMax:
				findAnotherMob = True
				break
			selectingAttempts += 1
			# Send selecting action
			Inject_SelectObject(mob['uid'])
			# Waits signal with timeout
			EventObjectSelected.wait(0.5)
		# Restart process
		if findAnotherMob:
			continue

		# Try to attack target
		skillID = skill['id']
		log("Plugin: Casting Skill \""+skill['name']+"\" to #"+str(SelectedUID))
		Inject_AttackTarget(SelectedUID,skillID)
		# We guess the skill has been activated
		Skills[skillID]['ready'] = False
		def SkillCooldownEnds(Skills,ID):
			# cooldown over, skill ready
			Skills[ID]['ready'] = True
		# Put skill on cooldown with some network delay
		Timer(skill['cool_down']/1000 + 0.1,SkillCooldownEnds,[Skills,skillID]).start()
		# Just waits casting time delay (as seconds)
		sleep(skill['cast_time']/1000)
	
	# Moves to starting position
	log('Plugin: Moving back to the center...')
	movementAttempts = 0
	movementAttemptsMax = 3
	while MoveToPosition(Position):
		movementAttempts += 1
		if movementAttempts >= movementAttemptsMax:
			break
		sleep(2.5)
	# Restart bot
	log('Plugin: "AttackInfinity" finished')
	start_bot()

# Returns the first drop around or None (pick filter is applied)
def FindDrop(Position,Radius):
	drops = get_drops()
	if drops:
		conn = GetFilterConnection()
		# Returns the first drop around pickable
		for uid, drop in drops.items():
			# Check radius
			if GetDistance(Position['x'],Position['y'],drop['x'],drop['y']) <= Radius:
				# Check if is pickable by pick filter
				if IsPickable(conn,drop['model']):
					drop['uid'] = uid
					conn.close()
					return drop
		conn.close()
	return None

# Pick up all drops around
def PickupDropsTask(Position,Radius):
	log("Plugin: Starting to pick up drops...")
	lastDropID = 0
	while True:

		# Find drop available
		drop = FindDrop(Position,Radius)
		if not drop:
			log('Plugin: No drops around!')
			break
		
		# Check if it's a new pick to show the log
		dropID = drop['uid']
		if lastDropID != dropID:
			log('Plugin: Picking up "'+drop['name']+'" (#'+str(dropID)+')')
			lastDropID = dropID
		
		# Pick up action
		Inject_PickUpItem(dropID)
		EventItemPickup.wait(2)

	# Moves to starting position
	log('Plugin: Moving back to the center...')
	movementAttempts = 0
	movementAttemptsMax = 3
	while MoveToPosition(Position):
		movementAttempts += 1
		if movementAttempts >= movementAttemptsMax:
			break
		sleep(2.5)
	# Restart bot
	log('Plugin: "PickupDrops" finished')
	start_bot()

# Returns the amount of members around you
def GetPartyMembersCount():
	# It will be counting myself
	party = get_party()
	if party:
		return len(party)
	return 1

# Waits for members around
def WaitPartyTask(MemberCount):
	log('Plugin: Waiting for #'+str(MemberCount)+' members to continue')
	while GetPartyMembersCount() < MemberCount:
		sleep(0.5)
	# Retart bot
	log('Plugin: Wait finished, all members are ready!')
	start_bot()

# Gets the npc data by using a lambda expression (name,servername)
def GetNPCByLambda(_lambda):
	# Check npcs around
	npcs = get_npcs()
	if npcs:
		for uid, npc in npcs.items():
			# Check expression
			if _lambda(npc['name'],npc['servername']):
				npc['uid'] = uid
				return npc
	return None

# Returns the battle of infinity defined level using the current character level
def GetInfinityLevel():
	level = get_character_data()['level']
	if level < 70:
		return 0
	if level > 70 and level <= 80:
		return 75
	if level > 80 and level <= 90:
		return 85
	if level > 90 and level <= 100:
		return 95
	if level > 100 and level <= 110:
		return 105
	return 0

# Gets the destination ID from teleport code name given
def GetTeleportIDByServerName(TeleportServerName):
	# connect to db
	conn = GetDatabaseConnection()
	# create command handler and execute it
	row = conn.cursor().execute('SELECT * FROM teleport WHERE servername LIKE ?',(TeleportServerName,)).fetchone()
	# close connection
	conn.close()
	if row:
		# returns destination id only
		return int(row[0])
	return 0

# Tries to enter to the battle infinity dungeon
def EnterInfinityTask(PartyMode,InfinityLevel):
	log('Plugin: Entering to Battle of Infinity...')
	global InfinityActivated
	InfinityActivated = False

	# Select NPC
	npc = GetNPCByLambda(lambda n,s: s == 'NPC_BATTLE_ARENA_MANAGER')
	while SelectedUID != npc['uid']:
		log('Plugin: Selecting "'+npc['name']+'"...')
		Inject_SelectObject(npc['uid'])
		EventObjectSelected.wait(1)

	# Create destination teleport name and teleports to the battle
	teleportServerName = 'GATE_MUHAN_'+('PARTY' if PartyMode else 'SOLO')+'_' +str(InfinityLevel)+'_01'
	destinationID = GetTeleportIDByServerName(teleportServerName)
	if destinationID:
		log('Plugin: Teleporting to Battle of Infinity ('+('PARTY' if PartyMode else 'SOLO')+') ['+str(InfinityLevel-4)+'~'+str(InfinityLevel+5)+']')
		Inject_UseTeleport(npc['uid'],destinationID)
		# Waits for teleport ready (2 minutes as max.)
		EventTeleported.wait(120)
		# Restart bot
		start_bot()
	else:
		log("Plugin: Destination ID from teleport not found!")

# Talks to dungeon manager to start the battle
def StartInfinityTask(NPCServerName):
	log('Plugin: Talking with Dungeon Manager...')
	global InfinityMaskEnabled
	InfinityMaskEnabled = False

	# Select NPC
	npc = GetNPCByLambda(lambda n,s: s == NPCServerName)
	while SelectedUID != npc['uid']:
		log('Plugin: Selecting "'+npc['name']+'"...')
		Inject_SelectObject(npc['uid'])
		EventObjectSelected.wait(1)

	# Start battle
	log('Plugin: Starting Battle of Infinity!')
	# CLIENT_MUHAN_ACTION_REQUEST
	inject_joymax(0x7588,b'\x01',False)
	# Close npc and restart bot
	Inject_CloseNPC(npc['uid'])
	start_bot()

# Talks to the NPC to use the mask mode
def TalkMorphstoneTask(NPCServerName,MaskMode,InfinityLevel):
	log('Plugin: Talking with Morphstone NPC...')
	# Just try to select NPC
	npc = GetNPCByLambda(lambda n,s: s == NPCServerName)
	Inject_SelectObject(npc['uid'])
	sleep(1)
	# CLIENT_MUHAN_ACTION_REQUEST
	inject_joymax(0x7588,struct.pack('<BI',3,npc['uid']))
	# Close npc and restart bot
	Inject_CloseNPC(npc['uid'])
	start_bot()

# Select object using his unique id
def Inject_SelectObject(UID):
	# CLIENT_SELECT_OBJECT_REQUEST
	inject_joymax(0x7045,struct.pack('<I',UID),False)

# Send skill action
def Inject_AttackTarget(TargetUID,SkillID=0):
	p = b'\x01' # flag
	if SkillID:
		p += b'\x04' # use skill action
		p += struct.pack('<I',SkillID)
	else:
		p += b'\x01' # use basic attack action
	# add target uid
	p += b'\x01'
	p += struct.pack('<I',TargetUID)
	# CLIENT_CHARACTER_ACTION_REQUEST
	inject_joymax(0x7074,p,False)

# Send pick up action to the dropped item
def Inject_PickUpItem(ItemUID,PetUID=0):
	if PetUID == 0:
		p = b'\x01' # flag
		p += b'\x02' # pick up action
		# add target uid
		p += b'\x01'
		p += struct.pack('<I',ItemUID)
		# CLIENT_CHARACTER_ACTION_REQUEST
		inject_joymax(0x7074,p,False)
	else:
		p = struct.pack('<I',PetUID)
		p += b'\x08' # pick up action
		p += struct.pack('<I',ItemUID)
		# CLIENT_CHARACTER_PET_ACTION_REQUEST
		inject_joymax(0x70C5,p,False)

# Sends the request to use a teleport
def Inject_UseTeleport(SourceUID,DestinationID):
	p = struct.pack('<I',SourceUID)
	p += b'\x02' # type
	p += struct.pack('<I',DestinationID)
	# CLIENT_TELEPORT_USE_REQUEST
	inject_joymax(0x705A,p,False)

# Sends the closing npc dialog request
def Inject_CloseNPC(NPCUID):
	# CLIENT_NPC_CLOSE_REQUEST
	inject_joymax(0x704B,struct.pack('<I',NPCUID),False)
# ______________________________ Events ______________________________ #

# Tries to enter to battle infinity by talking to NPC, and specifying the type
# Ex.: "EnterInfinity,party"
def EnterInfinity(args):
	# Set infinity mode
	global InfinityPartyMode
	InfinityPartyMode = False
	if len(args) >= 2:
		if args[1].lower() == 'party':
			InfinityPartyMode = True
	# Make sure the level is correct to use execute it
	infinityLevel = GetInfinityLevel()
	if not infinityLevel:
		log("Plugin: Your level didn't match with Battle of Infinity!")
		return 0
	# Check if NPC is around
	if GetNPCByLambda(lambda n,s: s == 'NPC_BATTLE_ARENA_MANAGER'):
		# Stop scripting
		stop_bot()
		# Avoid thread lock
		Timer(0.001,EnterInfinityTask,[InfinityPartyMode,infinityLevel]).start()
	else:
		log('Plugin: Battle Arena Manager is not near!')
	return 0


# Waits for party members count in the current position to continue script
# Ex.: "WaitParty,8"
def WaitParty(args):
	# Read member count
	memberCount = 8
	if len(args) >= 2:
		memberCount = round(float(args[1]))
	# Count to start waiting
	if GetPartyMembersCount() < memberCount:
		# Stop scripting
		stop_bot()
		# Starts waiting avoiding thread lock
		Timer(0.001,WaitPartyTask,[memberCount]).start()
	return 0

# Starts battle infinity by talking to the manager
# Ex.: "StartInfinity"
def StartInfinity(args):
	# Avoid using this command multiple times by bot
	if InfinityActivated:
		return 0
	# Make sure the level is correct to use execute it
	infinityLevel = GetInfinityLevel()
	if not infinityLevel:
		log("Plugin: Your level didn't match with Battle of Infinity!")
		return 0
	# Check if NPC is around
	managerServerName = 'NPC_MUHAN_'+('PARTY' if InfinityPartyMode else 'SOLO')+'_'+str(infinityLevel)+'_MANAGER'
	if GetNPCByLambda(lambda n,s: s == managerServerName):
		# Stop scripting
		stop_bot()
		# Avoid thread lock
		Timer(0.001,StartInfinityTask,[managerServerName]).start()
	else:
		log('Plugin: Dungeon Manager NPC is not near!')
	return 0

# Talks to the Morphstone NPC to converts you to the prefered state A/left is used by default.
# Ex.: "TalkMorphstone,B" or "TalkMorphstone,right"
def TalkMorphstone(args):
	# Avoid using this command multiple times by bot
	if InfinityMaskEnabled:
		return 0
	# Set mask used
	global InfinityMaskMode
	InfinityMaskMode = 'A'
	if len(args) >= 2:
		t = args[1].lower()  
		if t == 'b' or t == 'right':
			InfinityMaskMode = 'B'
	# Make sure the level is correct to use execute it
	infinityLevel = GetInfinityLevel()
	if not infinityLevel:
		log("Plugin: Your level didn't match with Battle of Infinity!")
		return 0
	# Check if NPC is around
	morphstoneServerName = 'NPC_MUHAN_CHANGE_'+('PARTY' if InfinityPartyMode else 'SOLO')+'_'+str(infinityLevel)+'_'+InfinityMaskMode
	if GetNPCByLambda(lambda n,s: s == morphstoneServerName):
		# Stop scripting
		stop_bot()
		# Avoid thread lock
		Timer(0.001,TalkMorphstoneTask,[morphstoneServerName,InfinityMaskMode,infinityLevel]).start()
	else:
		log('Plugin: Morphstone NPC is not near!')
	return 0

# Attacks all mobs around programatically using the radius and skills id provided
# Ex.: "AttackInfinity,100"
def AttackInfinity(args):
	# Check minimum requirements
	if len(args) < 2:
		log('Plugin: Error, not enough parameters to execute "AttackInfinity" command')
		return 0
	if not InfinityActivated:
		return 0
	# Stop scripting
	stop_bot()
	# Read radius from params
	radius = round(float(args[1]),2)
	# Make sure the level is correct to use execute it
	infinityLevel = GetInfinityLevel()
	if not infinityLevel:
		log("Plugin: Your level didn't match with Battle of Infinity!")
		return 0
	# Load skills from database for battle of infinity using the previous script commands used
	skillServerName = 'SKILL_MUHAN_'+('PARTY' if InfinityPartyMode else 'SOLO')+'_'+InfinityMaskMode+'_'+str(infinityLevel)+'_ATTACK0'
	conn = GetDatabaseConnection()
	rows = conn.cursor().execute('SELECT id FROM skills WHERE servername LIKE ? or servername LIKE ?',(skillServerName+'1',skillServerName+'2')).fetchall()
	conn.close()
	skills = []
	for row in rows:
		try:
			skills.append(int(row[0]))
		except Exception as e:
			log('Plugin: Error, Skill (#'+i+') ['+str(e)+']')
			continue
	# Load skills data
	skills = LoadSkills(skills)
	if not skills:
		log('Plugin: No skills found for attacking!')
		return 0
	# Current position used as center
	position = get_position()
	# Maximum delay for waiting mobs
	timeout = 45
	# Avoid thread lock
	Timer(0.001,AttackInfinityTask,[position,radius,skills,timeout]).start()
	return 0

# Pick up drops around using the range provided or 100 as default
# Ex.: "PickupDrops,100"
def PickupDrops(args):
	# Set pick radius
	radius = 100
	if len(args) >= 2:
		radius = round(float(args[1]),2)
	# Current position used as center
	position = get_position()
	# Check for drops
	if not FindDrop(position,radius):
		log('Plugin: No drops at this area')
		return 0
	# Stop scripting
	stop_bot()
	# Avoid thread lock
	Timer(0.001,PickupDropsTask,[position,radius]).start()
	return 0

# Removes the mask from morphstone if still activated
# Ex.: "RemoveMorphstone"
def RemoveMorphstone(args):
	buffs = get_active_skills()
	for skillID in buffs:
		buff = buffs[skillID]
		if buff['servername'].startswith('SKILL_MUHAN_'):
			log('Plugin: Trying to remove "'+buff['name']+'"')
			p = b'\x01'
			p += b'\x05' # Remove buff
			p += struct.pack('<I',skillID)
			# CLIENT_CHARACTER_ACTION_REQUEST
			inject_joymax(0x7074,p,False)
	return 0

# Called when the character teleports and right after joined_game()
def teleported():
	EventTeleported.set()
	EventTeleported.clear()

# Called when the character enters the game world
def joined_game():
	global character_data
	character_data = get_character_data()

# All packets received from game server will be passed to this function
# Returning True will keep the packet and False will not forward it to the game client
def handle_joymax(opcode, data):
	# SERVER_SELECT_OBJECT_RESPONSE
	if opcode == 0xB045:
		global SelectedUID
		# check success
		if data[0] == 1:
			SelectedUID = struct.unpack_from("<I",data,1)[0]
		else:
			SelectedUID = 0
		# Notify event
		EventObjectSelected.set()
		EventObjectSelected.clear()
	# SERVER_INVENTORY_ITEM_MOVEMENT
	elif opcode == 0xB034:
		# check success
		if data[0] == 1:
			# check pick up
			if data[1] == 6:
				# Notify event
				EventItemPickup.set()
				EventItemPickup.clear()
	# SERVER_MUHAN_ACTION_RESPONSE
	elif opcode == 0xB588:
		t = data[0]
		# Mask selection
		if t == 3:
			global InfinityMaskEnabled
			# Success
			if data[1] == 1:
				InfinityMaskEnabled = True
			else:
				InfinityMaskEnabled = False
	# SERVER_MUHAN_NOTICE
	elif opcode == 0x3592:
		if data[0] == 255:
			t = data[1] # type
			global InfinityActivated
			if t == 64:
				InfinityActivated = True
				log('Plugin: Battle of Infinity has started')
			elif t == 65:
				InfinityActivated = True
				log('Plugin: Battle of Infinity round #'+str(data[2]))
			elif t == 66:
				InfinityActivated = False
				log('Plugin: Battle of Infinity has ended')
	return True

# Plugin loaded
log('Plugin: '+pName+' v'+pVersion+' succesfully loaded')