from phBot import *
from threading import Timer
import phBotChat
import QtBind
import struct
import random
import json
import os

pName = 'xControl'
pVersion = '0.3.2'
pUrl = 'https://raw.githubusercontent.com/JellyBitz/phBot-xPlugins/master/xControl.py'

# Avoid issues
inGame = False

# Globals
followPlayer = ''
followDistance = 0

# Initializing GUI
gui = QtBind.init(__name__,pName)
lblxControl = QtBind.createLabel(gui,'Manage your partys easily using the ingame chat.\nThe Leader(s) is the character that write chat commands.\nIf you character have Leader(s) into the leader list, this will follow his orders.\n\n* UPPERCASE is required to use the command, all his data is separated by spaces.\n* #Variable (required) #Variable? (optional)\n Supported commands :\n - START : Start bot\n - STOP : Stop bot\n - TRACE #Player? : Start trace to leader or another character\n - NOTRACE : Stop trace\n - SETAREA : Set training area using the actual location\n - SIT : Sit or Stand up, depends\n - CAPE #Type? : Use PVP Cape\n - ZERK : Use berserker mode if is available\n - RETURN : Use some "Return Scroll" from your inventory\n - TELEPORT #A #B : Use teleport from location A to B\n - INJECT #Opcode #Encrypted? #Data : Inject packet\n - CHAT #Type #Message : Send any message type\n - MOVEON #Radius? : Set a random movement',21,11)
lblxControl2 = QtBind.createLabel(gui,' - FOLLOW #Player? #Distance? : Trace a party player using distance\n - NOFOLLOW : Stop following\n - PROFILE #Name? : Loads a profile by his name',345,101)

tbxLeaders = QtBind.createLineEdit(gui,"",511,11,100,20)
lstLeaders = QtBind.createList(gui,511,32,176,48)
btnAddLeader = QtBind.createButton(gui,'btnAddLeader_clicked',"    Add    ",612,10)
btnRemLeader = QtBind.createButton(gui,'btnRemLeader_clicked',"     Remove     ",560,79)

# Return xControl folder path
def getPath():
	return get_config_dir()+pName+"\\"

# Return character configs path (JSON)
def getConfig():
	return getPath()+get_character_data()['server'] + "_" + get_character_data()['name'] + ".json"

# Load default configs
def loadDefaultConfig():
	# Clear data
	QtBind.clear(gui,lstLeaders)

# Loads all config previously saved
def loadConfigs():
	loadDefaultConfig()
	# Check config exists to load
	if os.path.exists(getConfig()):
		data = {}
		with open(getConfig(),"r") as f:
			data = json.load(f)
		if "Leaders" in data:
			for nickname in data["Leaders"]:
				QtBind.append(gui,lstLeaders,nickname)

# Add leader to the list
def btnAddLeader_clicked():
	if inGame:
		player = QtBind.text(gui,tbxLeaders)
		# Player nickname it's not empty
		if player and not lstLeaders_exist(player):
			# Init dictionary
			data = {}
			# Load config if exist
			if os.path.exists(getConfig()):
				with open(getConfig(), 'r') as f:
					data = json.load(f)
			# Add new leader
			if not "Leaders" in data:
				data['Leaders'] = []
			data['Leaders'].append(player)
			# Replace configs
			with open(getConfig(),"w") as f:
				f.write(json.dumps(data, indent=4, sort_keys=True))
			QtBind.append(gui,lstLeaders,player)
			QtBind.setText(gui, tbxLeaders,"")
			log('Plugin: Leader added ['+player+']')

# Remove leader selected from list
def btnRemLeader_clicked():
	if inGame:
		selectedItem = QtBind.text(gui,lstLeaders)
		if selectedItem:
			if os.path.exists(getConfig()):
				data = {"Leaders":[]}
				with open(getConfig(), 'r') as f:
					data = json.load(f)
				try:
					# remove leader nickname from file if exists
					data["Leaders"].remove(selectedItem)
					with open(getConfig(),"w") as f:
						f.write(json.dumps(data, indent=4, sort_keys=True))
				except:
					pass # just ignore file if doesn't exist
			QtBind.remove(gui,lstLeaders,selectedItem)
			log('Plugin: Leader removed ['+selectedItem+']')

# Return True if nickname exist at the leader list
def lstLeaders_exist(nickname):
	players = QtBind.getItems(gui,lstLeaders)
	for i in range(len(players)):
		if players[i].lower() == nickname.lower():
			return True
	return False

# Called when the bot successfully connects to the game server
def connected():
	global inGame
	inGame = False

# Called when the character enters the game world
def joined_game():
	global inGame
	inGame = True
	loadConfigs()

# All chat messages received are sent to this function
def handle_chat(t,player,msg):
	if player:
		# Check player at leader list
		if lstLeaders_exist(player):
			# Parsing message command
			if msg == "START":
				start_bot()
				log("Plugin: Bot started")
			elif msg == "STOP":
				stop_bot()
				log("Plugin: Bot stopped")
			elif msg.startswith("TRACE"):
				if msg == "TRACE":
					if start_trace(player):
						log("Plugin: Starting trace to ["+player+"]")
				else:
					msg = msg[5:].split()
					if msg:
						if start_trace(msg[0]):
							log("Plugin: Starting trace to ["+msg[0]+"]")
			elif msg == "NOTRACE":
				stop_trace()
				log("Plugin: Trace stopped")
			elif msg == "SETAREA":
				p = get_position()
				set_training_position(p['region'], p['x'], p['y'])
				log("Plugin: Setting training area (X:%.1f,Y:%.1f)"%(p['x'],p['y']))
			elif msg == "SIT":
				log("Plugin: Sit/Stand")
				inject(["","704F","04"])
			elif msg.startswith("CAPE"):
				if msg == "CAPE":
					log("Plugin: Using PVP Cape (Yellow)")
					inject(["","7516","5"])
				else:
					type = msg[4:].split()
					if type:
						type = type[0].lower()
						if type == "off":
							log("Plugin: Removing PVP Cape")
							inject(["","7516","0"])
						elif type == "red":
							log("Plugin: Using PVP Cape (Red)")
							inject(["","7516","1"])
						elif type == "gray":
							log("Plugin: Using PVP Cape (Gray)")
							inject(["","7516","2"])
						elif type == "blue":
							log("Plugin: Using PVP Cape (Blue)")
							inject(["","7516","3"])
						elif type == "white":
							log("Plugin: Using PVP Cape (White)")
							inject(["","7516","4"])
						elif type == "yellow":
							log("Plugin: Using PVP Cape (Yellow)")
							inject(["","7516","5"])
						else:
							log("Plugin: Wrong PVP Cape color")
			elif msg == "ZERK":
				log("Plugin: Using Berserker mode")
				inject(["","70A7","1"])
			elif msg == "RETURN":
				# Trying avoid high CPU usage with many chars at the same time
				Timer(random.random(), inject_useReturnScroll).start()
			elif msg.startswith("TELEPORT"):
				msg = msg.split(' ',2)
				if msg and len(msg) == 3:
					inject_teleport(msg[1],msg[2])
			elif msg.startswith("INJECT"):
				inject(msg.split())
			elif msg.startswith("CHAT"):
				sendChatCommand(msg)
			elif msg.startswith("MOVEON"):
				if msg == "MOVEON":
					randomMovement()
				else:
					try:
						# split and parse movement radius
						radius = int(float(msg[6:].split()[0]))
						# to positive
						radius = (radius if radius > 0 else radius*-1)
						randomMovement(radius)
					except:
						log("Plugin: Movement maximum radius incorrect")
			elif msg.startswith("FOLLOW"):
				if msg == "FOLLOW":
					if start_follow(player):
						log("Plugin: Starting to follow to ["+player+"]")
				else:
					msg = msg[6:].split()
					try:
						if start_follow(msg[0],int(float(msg[1]))):
							log("Plugin: Starting to follow to ["+msg[0]+"] using ["+msg[1]+"] as distance")
					except:
						log("Plugin: Follow distance incorrect")
			elif msg == "NOFOLLOW":
				stop_follow()
				log("Plugin: Following stopped")
			elif msg.startswith("PROFILE"):
				if msg == "PROFILE":
					if set_profile('Default'):
						log("Plugin: Setting Default profile")
				else:
					msg = msg[7:].strip()
					if set_profile(msg):
						log("Plugin: Setting "+msg+" profile")

# Inject Packet (Use return scroll)
def inject_useReturnScroll():
	items = get_inventory()['items']
	for slot, item in enumerate(items):
		if item:
			if item['name'] == 'Return Scroll' or item['name'] == 'Special Return Scroll' or item['name'] == 'Token Return Scroll' or item['name'] == 'Beginner instant recall scroll' or item['name'] == 'Instant Return Scroll':
				Packet = bytearray()
				Packet.append(slot)
				Packet.append(0x30)
				Packet.append(0x0C) 
				Packet.append(0x03)
				Packet.append(0x01)
				inject_joymax(0x704C, Packet, True)
				log('Plugin: Using "'+item['name']+'"')
				return
	log('Plugin: "Return Scroll" not found at your inventory')

# Inject teleport packet, using the source and destination name
def inject_teleport(source,destination):
	t = get_teleport_data(source, destination)
	if t:
		npcs = get_npcs()
		for key, npc in npcs.items():
			if npc['name'] == source:
				log("Plugin: Selecting teleporter ["+source+"]")
				# Teleport found
				inject_joymax(0x7045, struct.pack('<I', key), False)
				# Start a timer to teleport in 2.0 seconds
				Timer(2.0, inject_joymax, (0x705A,struct.pack('<IBI', key, 2, t[1]),False)).start()
				Timer(2.0, log, ("Plugin: Teleporting to ["+destination+"]")).start()
				return
		log('Plugin: Teleport not found')
	else:
		log('Plugin: Wrong teleport name')

# Inject Packet, even through Script. All his data is separated by comma, encrypted will be false if it's not specified.
# Example 1: "inject,Opcode?,ItsEncrypted?,Data?,Data?,Data?,..."
# Example 2: "inject,3091,False,0" or "inject,3091,0" (means greet action)
def inject(args):
	if len(args) >= 3:
		opcode = int(args[1],16)
		encrypted = False
		dataPos = 2
		if args[2].lower() == "true" or args[2].lower() == "false":
			encrypted = True if args[2].lower() == "true" else False
			dataPos += 1
		Packet = bytearray()		
		for i in range(dataPos, len(args)):
			Packet.append(int(args[i],16))
		inject_joymax(opcode,Packet,encrypted)
		log("Plugin: Injecting packet")
		log("[Opcode:"+args[1]+"][Data:"+' '.join('{:02X}'.format(int(args[x],16)) for x in range(dataPos, len(args)))+"][Encrypted:"+("Yes" if encrypted else "No")+"]")
	else:
		log("Plugin: Incorrect structure to inject packet")
	return 0

# Send message, Ex. "CHAT All Hello World!" or "CHAT private JellyBitz Hi!"
def sendChatCommand(message):
	try:
		# Delete CHAT word
		message = message[4:].strip()
		# Parse type
		t = message.split(' ',1)
		# Check arguments length and empty message
		if len(t) == 2 and len(t[1]) > 0:
			success = False
			type = t[0].lower()
			if type == "all":
				success = phBotChat.All(t[1])
			elif type == "private":
				t = t[1].split(' ',1)
				success = phBotChat.Private(t[0],t[1])
			elif type == "party":
				success = phBotChat.Party(t[1])
			elif type == "guild":
				success = phBotChat.Guild(t[1])
			elif type == "union":
				success = phBotChat.Union(t[1])
			elif type == "note":
				t = t[1].split(' ',1)
				success = phBotChat.Private(t[0],t[1])
			elif type == "stall":
				success = phBotChat.Stall(t[1])
			if success:
				log("Plugin: Message sent successfully")
	except:
		log('Plugin: Incorrect structure to send message')

# Move to a random position from the actual position using a maximum radius
def randomMovement(radiusMax=10):
	# Generating a random new point
	pX = random.uniform(-radiusMax,radiusMax)
	pY = random.uniform(-radiusMax,radiusMax)
	# Mixing with the actual position
	p = get_position()
	pX = pX + p["x"]
	pY = pY + p["y"]
	# Moving to new position
	move_to(pX,pY,p["z"])
	log("Plugin: Random movement to (X:%.1f,Y:%.1f)"%(pX,pY))

# Follow a player using distance. Return success
def start_follow(player,distance=10):
	if party_player(player):
		global followPlayer,followDistance
		followPlayer = player
		followDistance = distance
		if not followPlayer:
			Timer(0.1, start_follow_loop).start()
		return True
	return False

# Return True if the player is in the party
def party_player(player):
	players = get_party()
	if players:
		for p in players:
			if players[p]['name'] == player:
				return True
	return False

# Return point [X,Y] if player is in the party and near, otherwise return None
def near_party_player(player):
	players = get_party()
	if players:
		for p in players:
			if players[p]['name'] == player and p['player_id'] > 0:
				return [players[p]['x'],players[p]['y']]
	return None

# Timer loop (1s) to keep following the player
def start_follow_loop():
	if inGame:
		if followPlayer:
			Timer(1.0, start_follow_loop).start()
			iniPoint = near_party_player(followPlayer)
			if iniPoint:
				finPoint = get_position()
				x = finPoint['x'] - iniPoint[0]
				y = finPoint['y'] - iniPoint[1]
				finDist = ( (x)**2 + (y)**2 )**0.5
				x = (followDistance * x) / finDist
				y = (followDistance * y) / finDist
				x += finPoint['x']
				y += finPoint['y']
				move_to(x,y,finPoint['z'])

# Stop follow player
def stop_follow():
	global followPlayer,followDistance
	followPlayer = ""
	followDistance = 0
	return True

# Plugin loaded success
log("Plugin: "+pName+" v"+pVersion+" successfully loaded")
# Creating xControl configs folder
if not os.path.exists(getPath()):
	os.makedirs(getPath())
	log('Plugin: "'+pName+'" folder has been created')