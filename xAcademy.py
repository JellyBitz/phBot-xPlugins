from phBot import *
import QtBind
from threading import Timer
import struct
import random
import json
import os
import subprocess

pName = 'xAcademy'
pVersion = '1.1.0'
pUrl = 'https://raw.githubusercontent.com/JellyBitz/phBot-xPlugins/master/xAcademy.py'

# User settings
SEQUENCE_DEFAULT_NUMBER = 100 # If Custom Nickname is set like "Jelly", it will try to create "Jelly100","Jelly101", ...
NOTIFICATION_SOUND_PATH = 'c:\\Windows\\Media\\chimes.wav'

# ______________________________ Initializing ______________________________ #

# Globals
isCreatingCharacter = False
CreatingNickname = ""

# Graphic user interface
gui = QtBind.init(__name__,pName)
cbxEnabled = QtBind.createCheckBox(gui,'cbxDoNothing','Enabled',6,10)

lblProfileName = QtBind.createLabel(gui,"Config profile name :",345,10)
tbxProfileName = QtBind.createLineEdit(gui,"",450,7,110,19)

btnSaveConfig = QtBind.createButton(gui,'btnSaveConfig_clicked',"  Save  ",570,3)
btnLoadConfig = QtBind.createButton(gui,'btnLoadConfig_clicked',"  Load  ",645,3)

lblNickname = QtBind.createLabel(gui,"Custom Nickname :",6,35)
tbxNickname = QtBind.createLineEdit(gui,"",100,32,102,19)

lblSequence = QtBind.createLabel(gui,"Number sequence :",6,55)
tbxSequence = QtBind.createLineEdit(gui,"",102,52,100,19)

lblRace = QtBind.createLabel(gui,"Custom Race :",6,75)
cmbxRace = QtBind.createCombobox(gui,79,72,123,19)
QtBind.append(gui,cmbxRace,"CH")
QtBind.append(gui,cmbxRace,"EU")

lblFullCharacters = QtBind.createLabel(gui,"The next action(s) will be executed if not possible create more characters :",6,100)
lblCMD = QtBind.createLabel(gui,"Run system command (CMD) :",15,120)
tbxCMD = QtBind.createLineEdit(gui,"",163,117,235,19)
cbxExit = QtBind.createCheckBox(gui,'cbxDoNothing','Close bot',15,140)
cbxNotification_Full = QtBind.createCheckBox(gui,'cbxDoNothing','Show phBot Notification',15,160)
cbxSound_Full = QtBind.createCheckBox(gui,'cbxDoNothing','Play sound.  Path : ',15,180)
tbxSound_Full = QtBind.createLineEdit(gui,'',128,179,270,19)
cbxLog_Full = QtBind.createCheckBox(gui,'cbxDoNothing','Log into a file',15,200)

# ______________________________ Methods ______________________________ #

# Return folder path
def getPath():
	return get_config_dir()+pName+"\\"

# Return character configs path (JSON)
def getConfig(name):
	if not name:
		name = pName;
	return getPath()+name+".json"

# Load default configs
def loadDefaultConfig():
	# Clear data
	QtBind.setText(gui,tbxProfileName,"")
	QtBind.setChecked(gui,cbxEnabled,False)

	QtBind.setText(gui,tbxNickname,"")
	QtBind.setText(gui,tbxSequence,str(SEQUENCE_DEFAULT_NUMBER))
	QtBind.setText(gui,cmbxRace,"CH")

	QtBind.setText(gui,tbxCMD,"")
	QtBind.setChecked(gui,cbxNotification_Full,False)
	QtBind.setChecked(gui,cbxSound_Full,False)
	QtBind.setText(gui,tbxSound_Full,NOTIFICATION_SOUND_PATH)
	QtBind.setChecked(gui,cbxLog_Full,False)

	QtBind.setChecked(gui,cbxExit,False)

# Loads all config previously saved
def loadConfigs(fileName=""):
	# Reset config
	loadDefaultConfig()
	# Check config exists to load
	if os.path.exists(getConfig(fileName)):
		data = {}
		with open(getConfig(fileName),"r") as f:
			data = json.load(f)

		# Load all data
		QtBind.setText(gui,tbxProfileName,fileName)

		if "Enabled" in data and data['Enabled']:
			QtBind.setChecked(gui,cbxEnabled,True)

		if "Nickname" in data:
			QtBind.setText(gui,tbxNickname,data["Nickname"])
		if "Sequence" in data and data["Sequence"]:
			QtBind.setText(gui,tbxSequence,data["Sequence"])
		if "Race" in data:
			QtBind.setText(gui,cmbxRace,data["Race"])

		if "CMD" in data:
			QtBind.setText(gui,tbxCMD,data["CMD"])
		if "NotificationFull" in data and data['NotificationFull']:
			QtBind.setChecked(gui,cbxNotification_Full,True)
		if "SoundFull" in data and data['SoundFull']:
			QtBind.setChecked(gui,cbxNotification_Full,True)
		if "SoundFullPath" in data and data["SoundFullPath"]:
			QtBind.setText(gui,tbxSound_Full,data["SoundFullPath"])
		if "LogFull" in data and data['LogFull']:
			QtBind.setChecked(gui,cbxLog_Full,True)

		if "Exit" in data and data['Exit']:
			QtBind.setChecked(gui,cbxExit,True)
		
		return True
	return False

# Save specific value at config
def saveConfigs(fileName=""):
	data = {}
	# Save all data
	data["Enabled"] = QtBind.isChecked(gui,cbxEnabled)

	data["Nickname"] = QtBind.text(gui,tbxNickname)
	sequence = QtBind.text(gui,tbxSequence)
	if sequence.isnumeric():
		data["Sequence"] = sequence
	else:
		data["Sequence"] = str(SEQUENCE_DEFAULT_NUMBER)
		QtBind.setText(gui,tbxSequence,data["Sequence"])
	data["Race"] = QtBind.text(gui,cmbxRace)

	data["CMD"] = QtBind.text(gui,tbxCMD)
	data["NotificationFull"] = QtBind.isChecked(gui,cbxNotification_Full)
	data["SoundFull"] = QtBind.isChecked(gui,cbxSound_Full)
	data["SoundFullPath"] = QtBind.text(gui,tbxSound_Full)
	data["LogFull"] = QtBind.isChecked(gui,cbxLog_Full)
	data["Exit"] = QtBind.isChecked(gui,cbxExit)
	# Overrides
	with open(getConfig(fileName),"w") as f:
		f.write(json.dumps(data,indent=4,sort_keys=True))

# Button event
def btnSaveConfig_clicked():
	# Check the config name
	strConfigName = QtBind.text(gui,tbxProfileName)
	saveConfigs(strConfigName)
	if strConfigName:
		log('Plugin: Profile ['+strConfigName+'] config has been saved')
	else:
		log("Plugin: Configs has been saved")

# Button event
def btnLoadConfig_clicked():
	# Check the config name
	strConfigName = QtBind.text(gui,tbxProfileName)
	if loadConfigs(strConfigName):
		if strConfigName:
			log("Plugin: Profile ["+strConfigName+"] config has been loaded")
		else:
			log("Plugin: Configs has been loaded")
	elif strConfigName:
		log("Plugin: Profile ["+strConfigName+"] not found")

# Create the character by injecting
def create_character():
	# select class
	race = QtBind.text(gui,cmbxRace)
	if race != 'EU':
		race = 'CH'

		model = get_monster_string('CHAR_CH_MAN_ADVENTURER')['model']
		chest = get_item_string('ITEM_CH_M_HEAVY_01_BA_A_DEF')['model']
		legs = get_item_string('ITEM_CH_M_HEAVY_01_LA_A_DEF')['model']
		shoes = get_item_string('ITEM_CH_M_HEAVY_01_FA_A_DEF')['model']
		weapon = get_item_string('ITEM_CH_SWORD_01_A_DEF')['model']
	else:
		race = 'EU'

		model = get_monster_string('CHAR_EU_MAN_NOBLE')['model']
		chest = get_item_string('ITEM_EU_M_HEAVY_01_BA_A_DEF')['model']
		legs = get_item_string('ITEM_EU_M_HEAVY_01_LA_A_DEF')['model']
		shoes = get_item_string('ITEM_EU_M_HEAVY_01_FA_A_DEF')['model']
		weapon = get_item_string('ITEM_EU_DAGGER_01_A_DEF')['model']

	if model == 0 or chest == 0 or legs == 0 or shoes == 0 or weapon == 0:
		log('Plugin: Error, the CodeName has changed on this server')
		return

	global isCreatingCharacter
	isCreatingCharacter = True
	log('Plugin: Creating character ['+CreatingNickname+'] ('+race+')')
	p = b'\x01'
	p += struct.pack('H', len(CreatingNickname))
	p += CreatingNickname.encode('ascii')
	p += struct.pack('I', model)
	p += struct.pack('B', 0)
	p += struct.pack('I', chest)
	p += struct.pack('I', legs)
	p += struct.pack('I', shoes)
	p += struct.pack('I', weapon)
	# Try to create character
	inject_joymax(0x7007,p, False)
	# Wait 3s to request character list
	Timer(3.0,inject_joymax,(0x7007, b'\x02', False)).start()

# Inject Packet
def Inject_DeleteCharacter(charName):
	p = b'\x03'
	p += struct.pack('H', len(charName))
	p += charName.encode('ascii')
	inject_joymax(0x7007,p, False)

# Inject Packet
def Inject_CheckName(charName):
	p = b'\x04'
	p += struct.pack('H', len(charName))
	p += charName.encode('ascii')
	inject_joymax(0x7007,p, False)

# Generate a random (male) game of thrones name!
def getRandomNick():
	# Adding names with max. 12 letters
	names = ["Aegon","Aerys","Aemon","Aeron","Alliser","Areo","Bran","Bronn","Benjen","Brynden","Beric","Balon","Bowen","Craster","Davos","Daario","Doran","Darrik","Dyron","Eddard","Edric","Euron","Edmure","Gendry","Gilly","Gregor","GreyWorm","Hoster","Jon","Jaime","Jorah","Joffrey","Jeor","Jaqen","Jojen","Janos","Kevan","Khal","Lancel","Loras","Maekar","Mace","Mance","Nestor","Oberyn","Petyr","Podrick","Quentyn","Robert","Robb","Ramsay","Roose","Rickon","Rickard","Rhaegar","Renly","Rodrik","Randyll","Samwell","Sandor","Stannis","Stefon","Tywin","Tyrion","Theon","Tormund","Trystane","Tommen","Val","Varys","Viserys","Victarion","Vimar","Walder","Wyman","Yoren","Yohn","Zane"]
	name = names[random.randint(0,len(names)-1)]
	# Fill with discord style
	if len(name) < 12:
		maxWidth = 12-len(name)
		if maxWidth > 4 :
			maxWidth = 4
		numbers = pow(10,maxWidth)-1
		name = str(name)+(str(random.randint(0,numbers))).zfill(maxWidth)
	return name

# Get the sequence previously saved or start a new one if not
def getSequence():	
	sequence = QtBind.text(gui,tbxSequence)
	# Check valid value
	if sequence.isnumeric():
		sequence = int(sequence)
	else:
		sequence = SEQUENCE_DEFAULT_NUMBER

	QtBind.setText(gui,tbxSequence,str(sequence+1))
	saveConfigs(QtBind.text(gui,tbxProfileName))
	
	return sequence

# Check the name length and sequence and return it
def getNickSequence(nickname):
	seq = str(getSequence())
	nick = nickname+seq
	nickLength = len(nick)
	if nickLength > 12: # as max. character restriction
		nickLength -= 12
		nick = nickname[:-nickLength]+seq
	return nick

# Check nickname if is available
def create_nickname():
	global CreatingNickname
	customName = QtBind.text(gui,tbxNickname) 
	if customName:
		CreatingNickname = getNickSequence(customName)
	else:
		CreatingNickname = getRandomNick()
	log("Plugin: Checking nickname ["+CreatingNickname+"]")
	Inject_CheckName(CreatingNickname)

# Close the bot process
def CloseBot():
	log("Plugin: Closing bot...")
	# Suicide :(
	os.kill(os.getpid(),9)

# ______________________________ Events ______________________________ #

# All packets received from game server will be passed to this function
# Returning True will keep the packet and False will not forward it to the game client
def handle_joymax(opcode,data):
	# SERVER_CHARACTER_SELECTION_RESPONSE
	if opcode == 0xB007 and QtBind.isChecked(gui,cbxEnabled):
		# Filter packet parsing
		locale = get_locale()
		try:
			global isCreatingCharacter
			index = 0 # cursor
			action = data[index]
			index+=1
			success = data[index]
			index+=1
			if action == 1:
				if isCreatingCharacter:
					isCreatingCharacter = False
					if success == 1:
						log("Plugin: Character created successfully!")
					else:
						log("Plugin: Character creation failed")
			elif action == 4:
				if isCreatingCharacter:
					if success == 1:
						log("Plugin: Nickname available!")
						create_character()
					else:
						log("Plugin: Nickname has been already taken!")
						Timer(1.0,create_nickname).start()
			elif action == 2:
				if success == 1:
					selectCharacter = ""
					deleteCharacter = ""
					deleteCharacterLevel = 0
					# Check all characters at selection screen
					nChars = data[index]
					index+=1
					log("Plugin: xAcademy character list: "+ ("None" if not nChars else ""))
					for i in range(nChars):
						index+=4 # model id
						# ReadAscii() / ushort (2) + string (length)
						charLength = struct.unpack_from('<H',data,index)[0]
						index+=2 # name length
						charName = struct.unpack_from('<' + str(charLength) + 's',data,index)[0].decode('cp1252')
						index+= charLength # name
						
						if locale == 18 or locale == 54:
							nickLength = struct.unpack_from('<H',data,index)[0]
							index+=2 # nick length
							nickName = struct.unpack_from('<' + str(nickLength) + 's',data,index)[0].decode('cp1252')
							index+= nickLength # nickname
						
						index+=1 # scale
						charLevel = data[index]
						index+=1 # level
						index+=8 # exp
						index+=2 # str
						index+=2 # int
						index+=2 # stats

						if locale == 18 or locale == 54:
							index+=4

						index+=4 # hp
						index+=4 # mp

						if locale == 18 or locale == 54:
							index+=2

						charIsDeleting = data[index]
						index+=1 # isDeleting
						if charIsDeleting:
							index+=4

						if locale == 18 or locale == 54:
							index+=4
						
						index+=1 # guildMemberClass
						# isGuildRenameRequired
						if data[index]:
							index+=1
							# guildName
							strLength = struct.unpack_from('<H', data, index)[0]
							index+=(2 + strLength)
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
						
						# Show info about previous character
						log(str(i+1)+") "+charName+" (Lv."+str(charLevel)+")"+(" [*]" if charIsDeleting else ""))

						# Conditions for auto select the first character
						if not selectCharacter:
							if charLevel < 40 and not charIsDeleting:
								selectCharacter = charName
						# Condition for deleting only one character
						if not deleteCharacter:
							if charLevel >= 40 and charLevel <= 50 and not charIsDeleting:
								deleteCharacter = charName
								deleteCharacterLevel = charLevel

					if locale == 18 or locale == 54:
						index+=1 # Removing warning

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
					if deleteCharacter:
						log("Plugin: deleting character ["+deleteCharacter+"] (Lv."+str(deleteCharacterLevel)+")")
						Timer(1.0,Inject_DeleteCharacter,(deleteCharacter,)).start()
					# Select or create character if is required
					if not selectCharacter:
						# Check the char limit
						if nChars < 4:
							isCreatingCharacter = True
							# Wait 10 seconds, then start looking for nicknames
							Timer(10.0,create_nickname).start()
						else:
							errMessage = "Plugin: Not enough space to create a new character!"
							log(errMessage)

							# Check actions
							cmd = QtBind.text(gui,tbxCMD)
							if cmd:
								log("Plugin: Trying to execute command ["+cmd+"]")
								# Run in subprocess to avoid lock it
								subprocess.Popen(cmd)

							# Try to show notification
							if QtBind.isChecked(gui,cbxNotification_Full):
								show_notification(pName+' v'+pVersion,errMessage)

							# Play sound
							if QtBind.isChecked(gui,cbxSound_Full):
								try:
									# Check if path has been set somehow
									path = QtBind.text(gui,tbxSound_Full)
									play_wav(path if path else NOTIFICATION_SOUND_PATH)
								except:
									pass

							# Log into the file
							if QtBind.isChecked(gui,cbxLog_Full):
								from datetime import datetime
								logText = datetime.now().strftime('%m/%d/%Y - %H:%M:%S')+': '+errMessage
								profileName = QtBind.text(gui,tbxProfileName)
								logText += '\nProfile being used: '+ (profileName if profileName else 'None')
								with open(getPath()+'_log.txt','a') as f:
									f.write(logText)

							# Exit from bot
							if QtBind.isChecked(gui,cbxExit):
								log("Plugin: Your bot will be closed at 5 seconds..")
								Timer(5.0,CloseBot).start()
					else:
						waitSelection = 1.0
						# Wait at least seconds after trying deleting a character
						if deleteCharacter != "":
							waitSelection += 5.0
						log("Plugin: Selecting character ["+selectCharacter+"] (lower than level 40)")
						Timer(waitSelection,select_character,(selectCharacter,)).start()
		except:
			log("Plugin: Oops! Parsing error.. "+pName+" cannot run at this server!")
			log("If you want support, send me all this via private message:")
			log("Data [" + ("None" if not data else ' '.join('{:02X}'.format(x) for x in data))+"] Locale ["+str(locale)+"]")
	return True

# Plugin loading ...
log('Plugin: '+pName+' v'+pVersion+' successfully loaded')

# Check configs folder
if os.path.exists(getPath()):
	useDefaultConfig = True 
	# Try to load config through command line
	bot_args = get_command_line_args()
	if bot_args:
		for i in range(len(bot_args)):
			param = bot_args[i].lower()
			if param.startswith('-xacademy-config='):
				# remove command
				configName = param[17:]
				# try to load config file
				if loadConfigs(configName):
					log("Plugin: "+pName+" profile ["+configName+"] loaded from commandline")
					useDefaultConfig = False
				else:
					log("Plugin: "+pName+" profile ["+configName+"] not found")
				break
	if useDefaultConfig:
		loadConfigs()

else:
	loadDefaultConfig()
	# Creating configs folder
	os.makedirs(getPath())
	log('Plugin: "'+pName+'" folder has been created')