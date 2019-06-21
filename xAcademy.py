from phBot import *
from threading import Timer
import struct
import random
import os

pName = 'xAcademy'
pVersion = '0.1.5'
pUrl = 'https://raw.githubusercontent.com/JellyBitz/phBot-xPlugins/master/xAcademy.py'

# Ex.: CUSTOM_NAME = "Jelly"
# will try to create "Jelly100","Jelly101","Jelly102"
CUSTOM_NAME = "" # Will be random if you leave it empty
SEQUENCE_START_NUMBER = 100
CUSTOM_RACE = "EU" # Will be random if you leave it empty

# Var to check if this plugin is creating the character
creatingCharacter = False
creatingCharacterNick = ""

# All packets received from Silkroad will be passed to this function
# Returning True will keep the packet and False will not forward it to the game server
def handle_joymax(opcode, data):
	# SERVER_CHARACTER_SELECTION_RESPONSE
	if opcode == 0xB007:
		locale = get_locale()
		# Filter packet parsing
		try:
			global creatingCharacter
			index = 0 # Packet index
			# ReadUInt8 / byte (1)
			action = data[index]
			index+=1
			success = data[index]
			index+=1
			if action == 1:
				if creatingCharacter:
					creatingCharacter = False
					if success:
						log("Plugin: Character created successfully!")
					else:
						log("Plugin: Character creation failed")
			elif action == 4:
				if creatingCharacter:
					if success:
						log("Plugin: Nickname available!")
						create_character()
					else:
						log("Plugin: Nickname has been already taken!")
						Timer(1.0,createNickname).start()
			elif action == 2:
				if success:
					selectCharacter = ""
					deleteCharacter = ""
					# Check all characters at selection screen
					nChars = data[index]
					index+=1
					log("Plugin: xAcademy character list: "+ ("None" if not nChars else ""))
					for i in range(nChars):
						# ReadUInt32() / uint (4)
						struct.unpack_from("<I",data,index)[0]
						index+=4 # model id
						# ReadAscii() / ushort (2) + string (length)
						charLength = struct.unpack_from('<H', data, index)[0]
						index+=2 # name length
						charName = struct.unpack_from('<' + str(charLength) + 's', data, index)[0].decode('cp1252')
						index+= charLength # name
						if locale == 18:
							index+=2 # ???
						index+=1 # scale
						charLevel = data[index]
						index+=1 # level
						exp = struct.unpack_from('<Q', data, index)[0]
						index+=8 # exp
						index+=2 # str
						index+=2 # int
						index+=2 # stats
						if locale == 18:
							unk01 = struct.unpack_from("<I",data,index)[0]
							index+=4 # ???
						index+=4 # hp
						index+=4 # mp
						if locale == 18:
							index+=2 # ???
						charIsDeleting = data[index]
						index+=1 # isDeleting
						if charIsDeleting:
							index+=4
						if locale == 18:
							index+=4 # ???
						index+=1 # guildMemberClass
						# isGuildRenameRequired
						if data[index]:
							index+=1
							# guildName
							strLength = struct.unpack_from('<H', data, index)[0]
							index+= (2 + strLength)
						else:
							index+=1
						index+=1 # academyMemberClass
						forCount = data[index]
						index+=1 # item count
						for j in range(forCount):
							index+=4 # RefItemID
							index+=1 # plus
						forCount = data[index]
						index+=1# avatar item count
						for j in range(forCount):
							index+=4 # RefItemID
							index+=1 # plus
						if locale == 18 and unk01 == 0:
							index+=1 # ???
						
						# Show info about previous character
						log(str(i+1)+") "+charName+" Lv."+str(charLevel)+(" (*)" if charIsDeleting else ""))

						# Conditions for auto select character
						if charLevel < 40 and not charIsDeleting:
							selectCharacter = charName
							break
						# Condition for deleting
						if charLevel >= 40 and charLevel <= 50 and not charIsDeleting:
							deleteCharacter = charName

					try:
						if i == (nChars-1):
							data[index]
							log("Plugin: [Warning] Packet partially parsed.")
					except:
						try:
							data[index-1]
							# Smooth parsing
						except:
							log("Plugin: [Warning] Packet partially parsed.")

					# Check for deleting a character
					if deleteCharacter != "":
						log("Plugin: deleting character ["+deleteCharacter+"] Lv."+str(charLevel))
						delete_character(deleteCharacter)
					else:
					# Select or create character if is required
						if selectCharacter == "":
							if nChars < 4:
								creatingCharacter = True
								# Wait 5 seconds, then start looking for a nickname
								Timer(5.0,createNickname).start()
							else:
								log("Plugin: Not enough space to create a new character")
						else:
							log("Plugin: Selecting character ["+selectCharacter+"] (lower than level 40)")
							select_character(selectCharacter);
		except:
			log("Plugin: Oops! Parsing error.. "+pName+" cannot run at this server!")
			log("If you want support, send me all this via private message:")
			log("Data [" + ("None" if not data else ' '.join('{:02X}'.format(x) for x in data))+"] Locale ["+str(locale)+"]")
	return True

def create_character():
	global creatingCharacterNick
	
	# select class
	charClass = CUSTOM_RACE
	if charClass == "":
		charClass = "CH" if random.randint(0,100)%2 == 0 else "EU"
	if charClass == 'CH':
		c_model = get_monster_string('CHAR_CH_MAN_ADVENTURER')['model']
		chest = get_item_string('ITEM_CH_M_HEAVY_01_BA_A_DEF')['model']
		legs = get_item_string('ITEM_CH_M_HEAVY_01_LA_A_DEF')['model']
		shoes = get_item_string('ITEM_CH_M_HEAVY_01_FA_A_DEF')['model']
		weapon = get_item_string('ITEM_CH_SWORD_01_A_DEF')['model']
	else:
		c_model = get_monster_string('CHAR_EU_MAN_NOBLE')['model']
		chest = get_item_string('ITEM_EU_M_HEAVY_01_BA_A_DEF')['model']
		legs = get_item_string('ITEM_EU_M_HEAVY_01_LA_A_DEF')['model']
		shoes = get_item_string('ITEM_EU_M_HEAVY_01_FA_A_DEF')['model']
		weapon = get_item_string('ITEM_EU_DAGGER_01_A_DEF')['model']

	if c_model == 0 or chest == 0 or legs == 0 or shoes == 0 or weapon == 0:
		log('Plugin: Could not retrieve item models')
		return

	creatingCharacter = True
	log('Plugin: Creating character with name %s and type %s' % (creatingCharacterNick, charClass))
	p = b'\x01'
	p += struct.pack('H', len(creatingCharacterNick))
	p += creatingCharacterNick.encode('ascii')
	p += struct.pack('I', c_model)
	p += struct.pack('B', 0)
	p += struct.pack('I', chest)
	p += struct.pack('I', legs)
	p += struct.pack('I', shoes)
	p += struct.pack('I', weapon)
	Timer(0.1,inject_joymax,(0x7007,p, False)).start()
	# Request char listing
	# CLIENT_CHARACTER_SELECTION_REQUEST
	Timer(5.0,inject_joymax,(0x7007, b'\x02', False)).start()

# Inject Packet
def delete_character(charName):
	p = b'\x03'
	p += struct.pack('H', len(charName))
	p += charName.encode('ascii')
	Timer(0.1,inject_joymax,(0x7007,p, False)).start()

# Inject Packet
def check_name(charName):
	p = b'\x04'
	p += struct.pack('H', len(charName))
	p += charName.encode('ascii')
	Timer(0.1,inject_joymax,(0x7007,p, False)).start()

# Generate a random nickname with max 12 characters 
def getRandomNick():
	names = ["Han","Je","Tuk","Zen","Jin","Xan","Xen","Xin","Za","Ke","Zoh","Zan","Zu","Lid","Yek","Ri","Riu","Ruk","Vi","Vik","Ki","Yi","Bok","Kah","Khan","War","Ten","Fu","Wan","Wi","Lin","Ran","Min","Ez","Kra","Ken"]
	# (36 subnames / 4 combinations : 58905 max possibilities at the moment)
	n1 = random.randint(0,len(names)-1)
	n2 = random.randint(0,len(names)-1)
	n3 = random.randint(0,len(names)-1)
	n4 = random.randint(0,len(names)-1)
	return (names[n1]+names[n2]+names[n3]+names[n4])

# Get the sequence previously saved or start a new one if not
def getSequence():
	seq = SEQUENCE_START_NUMBER -1
	if os.path.exists(pName+".Sequence.txt"):
		with open(pName+".Sequence.txt","r") as f:
			seq = int(f.read())
	seq += 1
	with open(pName+".Sequence.txt","w") as f:
		f.write(str(seq))
	return seq

# Check the name length and sequence and return it
def getNickSequence():
	seq = str(getSequence())
	nick = CUSTOM_NAME+seq
	nickLength = len(nick)
	if nickLength > 12: # as max. character restriction
		nickLength -= 12
		nick = CUSTOM_NAME[:-nickLength]+seq
	return nick

def createNickname():
	global creatingCharacterNick
	if CUSTOM_NAME != "":
		creatingCharacterNick = getNickSequence()
	else:
		creatingCharacterNick = getRandomNick()
	log("Plugin: Checking nickname ["+creatingCharacterNick+"]")
	check_name(creatingCharacterNick)

log('Plugin: '+pName+' v'+pVersion+' successfully loaded')