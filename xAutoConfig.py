from phBot import *
from threading import Timer
import shutil
import struct
import random
import os

pName = 'xAutoConfig'
pVersion = '0.2.0'
pUrl = 'https://raw.githubusercontent.com/JellyBitz/phBot-xPlugins/master/xAutoConfig.py'

# To know if this plugin is doing his job
creatingCharacter = False

# Called when the user successfully selects a character. No character data has been loaded yet.
def joined_game():
	# JSON config not found
	if not os.path.exists(get_config_path()):
		# JSON default configs path
		defaultConfig = get_config_dir()+"Default.json"
		if os.path.exists(defaultConfig):
			shutil.copyfile(defaultConfig,get_config_path())
			log("Plugin: Default JSON loaded")
		# db3 default filter path
		defaultFilter = get_config_dir()+"Default.db3"
		if os.path.exists(defaultFilter):
			shutil.copyfile(defaultFilter,get_config_path().replace(".json",".db3"))
			log("Plugin: Default Filter loaded")

# All packets received from Silkroad will be passed to this function
# Returning True will keep the packet and False will not forward it to the game server
def handle_joymax(opcode, data):
	# SERVER_CHARACTER_SELECTION_RESPONSE
	if opcode == 0xB007:
		index = 0 # Packet index
		# ReadUInt8 / byte (1)
		action = data[index]
		index+=1
		success = data[index]
		index+=1
		if action == 1:
			global creatingCharacter
			if creatingCharacter:
				creatingCharacter = False
				if success:
					log("Plugin: Character created successfully!")
				else:
					log("Plugin: Character creation failed!")
		elif action == 2:
			if success:
				selectCharacter = None
				deleteCharacter = None
				# Check all characters at selection screen
				nChars = data[index]
				index+=1
				for i in range(nChars):
					# ReadUInt32() / uint (4)
					struct.unpack_from("<i",data,index)[0] # model
					index+=4
					# ReadAscii() / ushort (2) + string (length)
					charLength = struct.unpack_from('<H', data, index)[0]
					index+= 2
					charName = struct.unpack_from('<' + str(charLength) + 's', data, index)[0].decode('cp1252')
					index+= charLength
					# Some unnecesary data will be skipped aggresively!
					index+=1 # scale
					charLevel = data[index]
					index+=23
					charIsDeleting = data[index]
					index+=1
					if charIsDeleting:
						index+=4
					index+=1
					if data[index]:
						index+=1
						strLength = struct.unpack_from('<H', data, index)[0]
						index+= (2 + strLength)
					else:
						index+=1
					index+=1
					forCount = data[index]
					for j in range(forCount):
						index+=5
					forCount = data[index]
					for j in range(forCount):
						index+=5

					# Conditions for auto select character
					if charLevel < 40 and not charIsDeleting:
						selectCharacter = charName
						break
					# Condition for deleting
					if charLevel > 40 and charLevel <= 50 and not charIsDeleting:
						deleteCharacter = deleteCharacter

				# Check for deleting a character
				if deleteCharacter:
					log("Plugin: deleting character ["+deleteCharacter+"] Lv."+charLevel)
					delete_character(deleteCharacter)
				# Check or create character if is required
				if selectCharacter == "":
					if nChars < 4:
						# Wait 5 seconds, then start creating character
						Timer(5.0,create_character).start()
					else:
						log("Plugin: Not enough space to create a new character")
				else:
					log("Plugin: Selecting character ["+selectCharacter+"] (lower than level 40)")
					select_character(selectCharacter)
	return True

def create_character():
	global creatingCharacter
	charName = getRandomName()
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
	log('Plugin: Creating character with name %s and type %s' % (charName, charClass))
	p = b'\x01'
	p += pack('H', len(charName))
	p += charName.encode('ascii')
	p += pack('I', c_model)
	p += pack('B', 0)
	p += pack('I', chest)
	p += pack('I', legs)
	p += pack('I', shoes)
	p += pack('I', weapon)
	Timer(0.1,inject_joymax,(0x7007,p, False)).start()
	# Request char listing
	# CLIENT_CHARACTER_SELECTION_REQUEST
	Timer(5.0,inject_joymax,(0x7007, b'\x02', False)).start()

# Select 4 subnames to create a new one
def getRandomName():
	names = ["Han","Je","Tuk","Zen","Jin","Xan","Xen","Xin","Za","Ke","Zoh","Zan","Zu","Lid","Yek","Ri","Riu","Ruk","Vi","Vik","Ki","Yi","Bok","Kah","Khan","War","Ten","Fu","Wan","Wi","Lin","Ran","Min","Ez","Kra","Ken"]
	# (36 subnames / 4 combinations : 58905 max possibilities at the moment)
	n1 = random.randint(0,len(names)-1)
	n2 = random.randint(0,len(names)-1)
	n3 = random.randint(0,len(names)-1)
	n4 = random.randint(0,len(names)-1)
	return (names[n1]+names[n2]+names[n3]+names[n4])

def delete_character(charName):
	p = b'\x03'
	p += pack('H', len(charName))
	p += charName.encode('ascii')
	Timer(0.1,inject_joymax,(0x7007,p, False)).start()

log('Plugin: '+pName+' v'+pVersion+' successfully loaded')