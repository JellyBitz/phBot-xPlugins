from phBot import *

pName = 'xArena'
pVersion = '0.0.1'
pUrl = 'https://raw.githubusercontent.com/JellyBitz/phBot-xPlugins/master/xArena.py'

def handle_joymax(opcode, data):
	if opcode == 0x34D2:
		if data[0] == 0xFF:
			result = data[1]
			if result == 0x00:
				log('Plugin: Successfully registered to arena')
				stop_bot()
			elif result == 0x02:
				log('Plugin: You already registered!')
			elif result == 0x04:
				log('Plugin: You may not register at this time')
			elif result == 0x06:
				log('Plugin: Match has been canceled duo to not enough players!')
			elif result == 0x0B:
				log("Plugin: Unable to register you're not in party")
			elif result == 0x0D:
				log("Plugin: You're not wearing the suit to register!")
		elif data[0] == 0x09:
			result = data[2]
			coins = data[3]
			log('Plugin: You have '+('lost' if result == 2 else 'won')+', you gained '+str(coins)+' coins!')
	return True

def arena(arguments):
	if len(arguments) < 3:
		log('Plugin: Missing arena type in the script')
		return 0

	t1 = arguments[1].lower()
	t2 = arguments[2].lower()
	NPCID = 0

	NPCs = get_npcs()
	for UniqueID, NPC in NPCs.items():
		if NPC['name'] == 'Arena Manager':
			NPCID = UniqueID
			break

	if NPCID == 0:
		log('Plugin: "Arena Manager" is not near. Be sure to use the script command near to the NPC')
	else:
		p = bytearray()
		# 1 = register; 2 = cancel
		p.append(0x01)

		# 0 = Random; 1 = Party; 2 = Guild (Only master can register); 3 = Job; 4 = CTF
		if t1 == 'random':
			p.append(0x00)
		elif t1 == 'party':
			p.append(0x01)
		elif t1 == 'guild':
			p.append(0x02)
		elif t1 == 'job':
			p.append(0x03)
		elif t1 == 'ctf':
			p.append(0x04)
		else:
			log('Plugin: Wrong Battle Arena type. Please be sure to select one: Random, Party, Guild, Job or CTF')
			return 0

		# 1 = Score; 2 = Flag;
		if t2 == 'score':
			p.append(0x01)
		elif t2 == 'flag':
			p.append(0x02)
		else:
			log('Plugin: Wrong Battle Arena type. Please be sure to select one: Score or Flag')
			return 0

		inject_joymax(0x74D3, p, False)
		return 500
	return 0

log('Plugin: '+pName+' v'+pVersion+' succesfully loaded')