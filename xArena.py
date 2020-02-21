from phBot import *
import struct

pName = 'xArena'
pVersion = '0.1.4'
pUrl = 'https://raw.githubusercontent.com/JellyBitz/phBot-xPlugins/master/xArena.py'

InBattleArena = False
InCTF = False
isPluginRegistering = False

def handle_joymax(opcode, data):
	global isPluginRegistering
	if opcode == 0x34D2:
		global InBattleArena
		if data[0] == 0xFF:
			result = data[1]
			if result == 0:
				log('Plugin: Successfully registered to arena')
				if isPluginRegistering:
					stop_bot()
			elif result == 2:
				log('Plugin: You already registered!')
			else:
				if result == 4:
					log('Plugin: You may not register at this time')
				elif result == 6:
					log('Plugin: Match has been canceled, not enough players!')
				elif result == 0x0B:
					log("Plugin: Unable to register you're not in party")
				elif result == 0x0D:
					log("Plugin: You're not wearing the suit to register!")
				isPluginRegistering = False
		elif data[0] == 8:
			InBattleArena = True
			if isPluginRegistering:
				log("Plugin: Activating Anti-AFK...")
				AntiAFK()
		elif data[0] == 9:
			result = data[2]
			coins = data[3]
			log('Plugin: You have '+('lost' if result == 2 else 'won')+', you gained '+str(coins)+' coins!')
			if InBattleArena:
				InBattleArena = False
				if isPluginRegistering:
					isPluginRegistering = False
					log("Plugin: Deactivating Anti-AFK. Starting bot...")
					start_bot()
	elif opcode == 0x34B1:
		global InCTF
		if data[0] == 0xFF:
			result = data[1]
			if result == 0:
				log('Plugin: Successfully registered to CTF')
				if isPluginRegistering:
					stop_bot()
			else:
				if result == 0x11:
					log('Plugin: You have won the match!')
				elif result == 0x16:
					log('Plugin: You have lost the match!')
				elif result == 0x17:
					log('Plugin: Match has ended in draw!')
				elif result == 0x06:
					log('Plugin: Match has been canceled, not enough players!')
				elif result == 0x15:
					log('Plugin: You are outside of the town!')
				isPluginRegistering = False
		elif data[0] == 8:
			InCTF = True
			if isPluginRegistering:
				log("Plugin: Activating Anti-AFK...")
				AntiAFK()
		elif data[0] == 9:
			result = data[2]
			if InCTF:
				InCTF = False
				log('Plugin: Capture The Flag event has ended')
				if isPluginRegistering:
					isPluginRegistering = False
					log("Plugin: Deactivating Anti-AFK. Starting bot...")
					start_bot()
	return True

# Gets the NPC unique ID if the specified name is found near
def GetNPCUniqueID(name):
	NPCs = get_npcs()
	if NPCs:
		name = name.lower()
		for UniqueID, NPC in NPCs.items():
			NPCName = NPC['name'].lower()
			if name in NPCName:
				return UniqueID
	return 0

# Register to the specified types "arena,type1,type2"
# Type 1; Random, Party, Guild or Job
# Type 2; Random, Score or Flag .. Or leave it empty if you are having issues (need test)
def arena(arguments):
	if len(arguments) < 2:
		log('Plugin: Missing arena type in the script')
		return 0
	
	NPCID = GetNPCUniqueID('Arena Manager')

	if NPCID == 0:
		log('Plugin: "Arena Manager" is not near. Be sure to use the script command near to the NPC')
	else:
		# read register type
		t1 = arguments[1].lower()
		t2 = ''
		if len(arguments) >= 3:
			t2 = arguments[2].lower()

		# 1 = register; 2 = cancel
		p = b'\x01'

		# 0 = Random; 1 = Party; 2 = Guild (Only master can register); 3 = Job;
		if t1 == 'random':
			p += struct.pack('B',0)
		elif t1 == 'party':
			p += struct.pack('B',1)
		elif t1 == 'guild':
			p += struct.pack('B',2)
		elif t1 == 'job':
			p += struct.pack('B',3)
		else:
			log('Plugin: Wrong Battle Arena type. Please be sure to select one: Random, Party, Guild or Job')
			return 0

		# 0 = random, 1 = Score; 2 = Flag;
		if t2 == '':
			pass
		elif t2 == 'score':
			p += struct.pack('B',1)
		elif t2 == 'flag':
			p += struct.pack('B',2)
		else:
			log('Plugin: Wrong Battle Arena type. Please be sure to select one: Score, or Flag')
			return 0

		global isPluginRegistering
		isPluginRegistering = True
		inject_joymax(0x74D3, p, False)
		return 500
	return 0

# Register to the captureflag event "capturetheflag"
def capturetheflag(arguments):
	NPCID = GetNPCUniqueID('So-Ok')
	if NPCID == 0:
		log('Plugin: NPC "So-Ok" is not near. Be sure to use the script command near to the NPC')
	else:
		p = bytearray()

		global isPluginRegistering
		isPluginRegistering = True
		inject_joymax(0x74B2, p, False)
		return 500
	return 0

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

# Anti AFK system by random movement
def AntiAFK():
	if InBattleArena or InCTF:
		#inject_joymax(0x3091,b'\x01', False)
		randomMovement(2)
		Timer(5.0, AntiAFK).start()

log('Plugin: '+pName+' v'+pVersion+' succesfully loaded')