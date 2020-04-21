from phBot import *
import QtBind
from threading import Timer
import json
import os

pVersion = '1.0.1'
pName = 'xAutoDungeon'
pUrl = 'https://raw.githubusercontent.com/JellyBitz/phBot-xPlugins/master/xAutoDungeon.py'

# ______________________________ Initializing ______________________________ #

# Globals
DEFAULT_CHECK_DELAY = 1.0 # seconds

# Graphic user interface
gui = QtBind.init(__name__,pName)

lblMobs = QtBind.createLabel(gui,'#   Add monster names to ignore    #\n#          from Monster Counter         #',31,3)
tbxMobs = QtBind.createLineEdit(gui,"",31,35,100,20)
lstMobs = QtBind.createList(gui,31,56,176,206)
btnAddMob = QtBind.createButton(gui,'btnAddMob_clicked',"    Add    ",132,34)
btnRemMob = QtBind.createButton(gui,'btnRemMob_clicked',"     Remove     ",80,261)

lblMonsterCounter = QtBind.createLabel(gui,"#                 Monster Counter                 #",520,3)
lstMonsterCounter = QtBind.createList(gui,520,23,197,239)
QtBind.append(gui,lstMonsterCounter,'Name (Type)') # Header

lblPreferences = QtBind.createLabel(gui,"#    Monster Counter preferences (By priority)    #",240,3)
lstIgnore = []
lstOnlyCount = []

lblGeneral = QtBind.createLabel(gui,'General (0)',240,30)
cbxIgnoreGeneral = QtBind.createCheckBox(gui,'cbxIgnoreGeneral_clicked','Ignore',345,30)
cbxOnlyCountGeneral = QtBind.createCheckBox(gui,'cbxOnlyCountGeneral_clicked','Only Count',405,30)

lblChampion = QtBind.createLabel(gui,'Champion (1)',240,49)
cbxIgnoreChampion = QtBind.createCheckBox(gui,'cbxIgnoreChampion_clicked','Ignore',345,49)
cbxOnlyCountChampion = QtBind.createCheckBox(gui,'cbxOnlyCountChampion_clicked','Only Count',405,49)

lblGiant = QtBind.createLabel(gui,'Giant (4)',240,68)
cbxIgnoreGiant = QtBind.createCheckBox(gui,'cbxIgnoreGiant_clicked','Ignore',345,68)
cbxOnlyCountGiant = QtBind.createCheckBox(gui,'cbxOnlyCountGiant_clicked','Only Count',405,68)

lblTitan = QtBind.createLabel(gui,'Titan (5)',240,87)
cbxIgnoreTitan = QtBind.createCheckBox(gui,'cbxIgnoreTitan_clicked','Ignore',345,87)
cbxOnlyCountTitan = QtBind.createCheckBox(gui,'cbxOnlyCountTitan_clicked','Only Count',405,87)

lblStrong = QtBind.createLabel(gui,'Strong (6)',240,106)
cbxIgnoreStrong = QtBind.createCheckBox(gui,'cbxIgnoreStrong_clicked','Ignore',345,106)
cbxOnlyCountStrong = QtBind.createCheckBox(gui,'cbxOnlyCountStrong_clicked','Only Count',405,106)

lblElite = QtBind.createLabel(gui,'Elite (7)',240,125)
cbxIgnoreElite = QtBind.createCheckBox(gui,'cbxIgnoreElite_clicked','Ignore',345,125)
cbxOnlyCountElite = QtBind.createCheckBox(gui,'cbxOnlyCountElite_clicked','Only Count',405,125)

lblUnique = QtBind.createLabel(gui,'Unique (8)',240,144)
cbxIgnoreUnique = QtBind.createCheckBox(gui,'cbxIgnoreUnique_clicked','Ignore',345,144)
cbxOnlyCountUnique = QtBind.createCheckBox(gui,'cbxOnlyCountUnique_clicked','Only Count',405,144)

lblParty = QtBind.createLabel(gui,'Party (16)',240,163)
cbxIgnoreParty = QtBind.createCheckBox(gui,'cbxIgnoreParty_clicked','Ignore',345,163)
cbxOnlyCountParty = QtBind.createCheckBox(gui,'cbxOnlyCountParty_clicked','Only Count',405,163)

lblChampionParty = QtBind.createLabel(gui,'ChampionParty (17)',240,182)
cbxIgnoreChampionParty = QtBind.createCheckBox(gui,'cbxIgnoreChampionParty_clicked','Ignore',345,182)
cbxOnlyCountChampionParty = QtBind.createCheckBox(gui,'cbxOnlyCountChampionParty_clicked','Only Count',405,182)

lblGiantParty = QtBind.createLabel(gui,'GiantParty (20)',240,201)
cbxIgnoreGiantParty = QtBind.createCheckBox(gui,'cbxIgnoreGiantParty_clicked','Ignore',345,201)
cbxOnlyCountGiantParty = QtBind.createCheckBox(gui,'cbxOnlyCountGiantParty_clicked','Only Count',405,201)

# ______________________________ Methods ______________________________ #

def cbxIgnoreGeneral_clicked(checked):
	Checkbox_Checked(checked,"lstIgnore",'0') # 0 = General
def cbxOnlyCountGeneral_clicked(checked):
	Checkbox_Checked(checked,"lstOnlyCount",'0')

def cbxIgnoreChampion_clicked(checked):
	Checkbox_Checked(checked,"lstIgnore",'1') # 1 = Champion
def cbxOnlyCountChampion_clicked(checked):
	Checkbox_Checked(checked,"lstOnlyCount",'1')

def cbxIgnoreGiant_clicked(checked):
	Checkbox_Checked(checked,"lstIgnore",'4') # 4 = Giant
def cbxOnlyCountGiant_clicked(checked):
	Checkbox_Checked(checked,"lstOnlyCount",'4')

def cbxIgnoreTitan_clicked(checked):
	Checkbox_Checked(checked,"lstIgnore",'5') # 5 = Titan
def cbxOnlyCountTitan_clicked(checked):
	Checkbox_Checked(checked,"lstOnlyCount",'5')

def cbxIgnoreStrong_clicked(checked):
	Checkbox_Checked(checked,"lstIgnore",'6') # 6 = Strong
def cbxOnlyCountStrong_clicked(checked):
	Checkbox_Checked(checked,"lstOnlyCount",'6')

def cbxIgnoreElite_clicked(checked):
	Checkbox_Checked(checked,"lstIgnore",'7') # 7 = Elite
def cbxOnlyCountElite_clicked(checked):
	Checkbox_Checked(checked,"lstOnlyCount",'7')

def cbxIgnoreUnique_clicked(checked):
	Checkbox_Checked(checked,"lstIgnore",'8') # 8 = Unique
def cbxOnlyCountUnique_clicked(checked):
	Checkbox_Checked(checked,"lstOnlyCount",'8')

def cbxIgnoreParty_clicked(checked):
	Checkbox_Checked(checked,"lstIgnore",'16') # 16 = Party
def cbxOnlyCountParty_clicked(checked):
	Checkbox_Checked(checked,"lstOnlyCount",'16')

def cbxIgnoreChampionParty_clicked(checked):
	Checkbox_Checked(checked,"lstIgnore",'17') # 17 = ChampionParty
def cbxOnlyCountChampionParty_clicked(checked):
	Checkbox_Checked(checked,"lstOnlyCount",'17')

def cbxIgnoreGiantParty_clicked(checked):
	Checkbox_Checked(checked,"lstIgnore",'20') # 20 = GiantParty
def cbxOnlyCountGiantParty_clicked(checked):
	Checkbox_Checked(checked,"lstOnlyCount",'20')

# Generalizing checkbox methods
def Checkbox_Checked(checked,gListName,mobType):
	gListReference = globals()[gListName]
	if checked:
		gListReference.append(mobType)
	else:
		gListReference.remove(mobType)
	saveConfig(gListName,gListReference)

# Return folder path
def getPath():
	return get_config_dir()+pName+"\\"

# Return character configs path (JSON)
def getConfig():
	return getPath()+pName+".json"

# Load config if exists
def loadConfigs():
	if os.path.exists(getConfig()):
		data = {}
		with open(getConfig(),"r") as f:
			data = json.load(f)
		# Check to load config
		if "lstMobs" in data:
			for d in data["lstMobs"]:
				QtBind.append(gui,lstMobs,d)
		if "lstIgnore" in data:
			global lstIgnore
			lstIgnore = data["lstIgnore"]
			for i in range(len(lstIgnore)):
				if lstIgnore[i] == '8':
					QtBind.setChecked(gui,cbxIgnoreUnique,True)
				elif lstIgnore[i] == '7':
					QtBind.setChecked(gui,cbxIgnoreElite,True)
				elif lstIgnore[i] == '6':
					QtBind.setChecked(gui,cbxIgnoreStrong,True)
				elif lstIgnore[i] == '5':
					QtBind.setChecked(gui,cbxIgnoreTitan,True)
				elif lstIgnore[i] == '4':
					QtBind.setChecked(gui,cbxIgnoreGiant,True)
				elif lstIgnore[i] == '1':
					QtBind.setChecked(gui,cbxIgnoreChampion,True)
				elif lstIgnore[i] == '0':
					QtBind.setChecked(gui,cbxIgnoreGeneral,True)
				elif lstIgnore[i] == '16':
					QtBind.setChecked(gui,cbxIgnoreParty,True)
				elif lstIgnore[i] == '17':
					QtBind.setChecked(gui,cbxIgnoreChampionParty,True)
				elif lstIgnore[i] == '20':
					QtBind.setChecked(gui,cbxIgnoreGiantParty,True)
		if "lstOnlyCount" in data:
			global lstOnlyCount
			lstOnlyCount = data["lstOnlyCount"]
			for i in range(len(lstOnlyCount)):
				if lstOnlyCount[i] == '8':
					QtBind.setChecked(gui,cbxOnlyCountUnique,True)
				elif lstOnlyCount[i] == '7':
					QtBind.setChecked(gui,cbxOnlyCountElite,True)
				elif lstOnlyCount[i] == '6':
					QtBind.setChecked(gui,cbxOnlyCountStrong,True)
				elif lstOnlyCount[i] == '5':
					QtBind.setChecked(gui,cbxOnlyCountTitan,True)
				elif lstOnlyCount[i] == '4':
					QtBind.setChecked(gui,cbxOnlyCountGiant,True)
				elif lstOnlyCount[i] == '1':
					QtBind.setChecked(gui,cbxOnlyCountChampion,True)
				elif lstOnlyCount[i] == '0':
					QtBind.setChecked(gui,cbxOnlyCountGeneral,True)
				elif lstOnlyCount[i] == '16':
					QtBind.setChecked(gui,cbxOnlyCountParty,True)
				elif lstOnlyCount[i] == '17':
					QtBind.setChecked(gui,cbxOnlyCountChampionParty,True)
				elif lstOnlyCount[i] == '20':
					QtBind.setChecked(gui,cbxOnlyCountGiantParty,True)

# Save specific value at config
def saveConfig(key,value):
	if key:
		data = {}
		if os.path.exists(getConfig()):
			with open(getConfig(),"r") as f:
				data = json.load(f)
		data[key] = value
		with open(getConfig(),"w") as f:
			f.write(json.dumps(data, indent=4, sort_keys=True))

# Add mob to the list
def btnAddMob_clicked():
	text = QtBind.text(gui,tbxMobs)
	if text and not QtBind_ItemsContains(text,lstMobs):
		QtBind.append(gui,lstMobs,text)
		QtBind.setText(gui,tbxMobs,"")
		saveConfig("lstMobs",QtBind.getItems(gui,lstMobs))
		log('Plugin: Monster added ['+text+']')

# Add mob to the list
def btnRemMob_clicked():
	selected = QtBind.text(gui,lstMobs)
	if selected and QtBind_ItemsContains(selected,lstMobs):
		QtBind.remove(gui,lstMobs,selected)
		saveConfig("lstMobs",QtBind.getItems(gui,lstMobs))
		log('Plugin: Monster removed ['+selected+']')

# Return True if text exist at the list
def ListContains(text,lst):
	for i in range(len(lst)):
		if lst[i].lower() == text.lower():
			return True
	return False

# Return True if item exists
def QtBind_ItemsContains(text,lst):
	return ListContains(text,QtBind.getItems(gui,lst))

# Attacking mobs using all configs from bot
def AttackMobs(wait,isAttacking,x,y,z,radius):
	count = getMobCount(radius)
	if count > 0:
		# Start to kill mobs using bot
		if isAttacking:
			log("Plugin: Killing ("+str(count)+") mobs at this area.")
		else:
			start_bot()
			log("Plugin: Starting to kill ("+str(count)+") mobs at this area. Radius: "+(str(radius) if radius != None else "Max."))
		# Check if there is not mobs to continue script
		Timer(wait,AttackMobs,(wait,True,x,y,z,radius)).start()
	else:
		# All mobs killed, stop botting
		stop_bot()
		# Setting training area far away. The bot should continue where he was at the script
		set_training_position(0,0,0)
		# Move back to the starting point
		move_to(x,y,z)
		log("Plugin: All mobs killed.. Getting back to the script.")
		# give it some time to reach the movement
		Timer(2.5,start_bot).start()

# Count all mobs around your character (60 or more it's the max. range I think)
def getMobCount(radius):
	# Clear
	QtBind.clear(gui,lstMonsterCounter)
	QtBind.append(gui,lstMonsterCounter,'Name (Type)') # Header
	count = 0
	# Get my position to calc radius
	p = get_position() if radius != None else None
	# Check all mob around
	monsters = get_monsters()
	if monsters:
		for key, mob in monsters.items():
			# Ignore if this mob type is found
			if ListContains(str(mob['type']),lstIgnore):
				continue
			# Only count setup
			if len(lstOnlyCount) > 0:
				# If is not in only count, skip it
				if not ListContains(str(mob['type']),lstOnlyCount):
					continue
			# Ignore mob names
			elif QtBind_ItemsContains(mob['name'],lstMobs):
				continue
			# Checking radius
			if radius != None:
				if round(GetDistance(p['x'], p['y'],mob['x'],mob['y']),2) > radius:
					continue
			# Adding GUI for a complete UX
			QtBind.append(gui,lstMonsterCounter,mob['name']+' ('+str(mob['type'])+')')
			count+=1
	return count

# Calc the distance from point A to B
def GetDistance(ax,ay,bx,by):
	return ((bx-ax)**2 + (by-ay)**2)**(0.5)

# ______________________________ Events ______________________________ #

# Attack all mobs around using the bot config. Ex: "AttackArea" or "AttackArea,5" or "AttackArea,5,75"
# Will be checking mobs every 5 seconds at the area as default.
# Will be using radius maximum (75 approx) as default
def AttackArea(args):
	# radius maximum as default
	radius = None
	if len(args) >= 2:
		radius = round(float(args[1]),2)
	# stop bot and kill mobs through bot
	if getMobCount(radius) > 0:
		# stop scripting
		stop_bot()
		# set automatically the training area
		p = get_position()
		set_training_position(p['region'], p['x'], p['y'])
		# set automatically the radius to avoid setting conflict
		if radius != None:
			set_training_radius(radius)
		else:
			set_training_radius(100.0)
		# checking mobs delay
		wait = DEFAULT_CHECK_DELAY
		if len(args) >= 3 and float(args[2]) > 0:
			wait = float(args[2])
		# start to kill mobs on other thread because interpreter lock
		Timer(0.1,AttackMobs,(wait,False,p['x'],p['y'],p['z'],radius)).start()
	# otherwise continue normally
	else:
		log("Plugin: No mobs at this area. Radius: "+(str(radius) if radius != None else "Max."))
	return 0

# Plugin loaded
log('Plugin: '+pName+' v'+pVersion+' succesfully loaded')

if os.path.exists(getPath()):
	# Adding RELOAD plugin support
	try:
		loadConfigs()
	except:
		# Just in case omg -_-
		log('Plugin: Error loading '+pName+' config file')
else:
	# Creating configs folder
	os.makedirs(getPath())
	log('Plugin: '+pName+' folder has been created')