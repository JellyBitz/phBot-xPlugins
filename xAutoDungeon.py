from phBot import *
import QtBind
from threading import Timer
import json
import os

pVersion = '0.3.2'
pName = 'xAutoDungeon'
pUrl = 'https://raw.githubusercontent.com/JellyBitz/phBot-xPlugins/master/xAutoDungeon.py'

# Initializing GUI
gui = QtBind.init(__name__,pName)

lblMobs = QtBind.createLabel(gui,'#    Add monster names to avoid    #\n#          from Monster counter         #',511,11)
tbxMobs = QtBind.createLineEdit(gui,"",511,43,100,20)
lstMobs = QtBind.createList(gui,511,64,176,198)
btnAddMob = QtBind.createButton(gui,'btnAddMob_clicked',"    Add    ",612,42)
btnRemMob = QtBind.createButton(gui,'btnRemMob_clicked',"     Remove     ",560,261)

lblPreferences = QtBind.createLabel(gui,"Monster counter preferences (Orderer by priority) :",21,11)
lstAvoid = []
lstOnly = []

lblUnique = QtBind.createLabel(gui,'Unique',21,30)
cbxAvoidUnique = QtBind.createCheckBox(gui,'cbxAvoidUnique_clicked','Avoid',80,30)
cbxOnlyUnique = QtBind.createCheckBox(gui,'cbxOnlyUnique_clicked','Only',150,30)
def cbxAvoidUnique_clicked(checked):
	Checkbox_Checked(checked,lstAvoid,"lstAvoid",'8') # 8 = Unique
def cbxOnlyUnique_clicked(checked):
	Checkbox_Checked(checked,lstOnly,"lstOnly",'8')

lblElite = QtBind.createLabel(gui,'Elite',21,49)
cbxAvoidElite = QtBind.createCheckBox(gui,'cbxAvoidElite_clicked','Avoid',80,49)
cbxOnlyElite = QtBind.createCheckBox(gui,'cbxOnlyElite_clicked','Only',150,49)
def cbxAvoidElite_clicked(checked):
	Checkbox_Checked(checked,lstAvoid,"lstAvoid",'7') # 7 = Elite
def cbxOnlyElite_clicked(checked):
	Checkbox_Checked(checked,lstOnly,"lstOnly",'7')

lblStrong = QtBind.createLabel(gui,'Strong',21,68)
cbxAvoidStrong = QtBind.createCheckBox(gui,'cbxAvoidStrong_clicked','Avoid',80,68)
cbxOnlyStrong = QtBind.createCheckBox(gui,'cbxOnlyStrong_clicked','Only',150,68)
def cbxAvoidStrong_clicked(checked):
	Checkbox_Checked(checked,lstAvoid,"lstAvoid",'6') # 6 = Strong
def cbxOnlyStrong_clicked(checked):
	Checkbox_Checked(checked,lstOnly,"lstOnly",'6')

lblTitan = QtBind.createLabel(gui,'Titan',21,87)
cbxAvoidTitan = QtBind.createCheckBox(gui,'cbxAvoidTitan_clicked','Avoid',80,87)
cbxOnlyTitan = QtBind.createCheckBox(gui,'cbxOnlyTitan_clicked','Only',150,87)
def cbxAvoidTitan_clicked(checked):
	Checkbox_Checked(checked,lstAvoid,"lstAvoid",'5') # 5 = Titan
def cbxOnlyTitan_clicked(checked):
	Checkbox_Checked(checked,lstOnly,"lstOnly",'5')

lblGiant = QtBind.createLabel(gui,'Giant',21,106)
cbxAvoidGiant = QtBind.createCheckBox(gui,'cbxAvoidGiant_clicked','Avoid',80,106)
cbxOnlyGiant = QtBind.createCheckBox(gui,'cbxOnlyGiant_clicked','Only',150,106)
def cbxAvoidGiant_clicked(checked):
	Checkbox_Checked(checked,lstAvoid,"lstAvoid",'4') # 4 = Giant
def cbxOnlyGiant_clicked(checked):
	Checkbox_Checked(checked,lstOnly,"lstOnly",'4')

lblChampion = QtBind.createLabel(gui,'Champion',21,125)
cbxAvoidChampion = QtBind.createCheckBox(gui,'cbxAvoidChampion_clicked','Avoid',80,125)
cbxOnlyChampion = QtBind.createCheckBox(gui,'cbxOnlyChampion_clicked','Only',150,125)
def cbxAvoidChampion_clicked(checked):
	Checkbox_Checked(checked,lstAvoid,"lstAvoid",'1') # 1 = Champion
def cbxOnlyChampion_clicked(checked):
	Checkbox_Checked(checked,lstOnly,"lstOnly",'1')

lblGeneral = QtBind.createLabel(gui,'General',21,144)
cbxAvoidGeneral = QtBind.createCheckBox(gui,'cbxAvoidGeneral_clicked','Avoid',80,144)
cbxOnlyGeneral = QtBind.createCheckBox(gui,'cbxOnlyGeneral_clicked','Only',150,144)
def cbxAvoidGeneral_clicked(checked):
	Checkbox_Checked(checked,lstAvoid,"lstAvoid",'0') # 0 = General
def cbxOnlyGeneral_clicked(checked):
	Checkbox_Checked(checked,lstOnly,"lstOnly",'0')

lblParty = QtBind.createLabel(gui,'Party',21,163)
cbxAvoidParty = QtBind.createCheckBox(gui,'cbxAvoidParty_clicked','Avoid',80,163)
cbxOnlyParty = QtBind.createCheckBox(gui,'cbxOnlyParty_clicked','Only',150,163)
def cbxAvoidParty_clicked(checked):
	Checkbox_Checked(checked,lstAvoid,"lstAvoid",'16') # 16 = Party
def cbxOnlyParty_clicked(checked):
	Checkbox_Checked(checked,lstOnly,"lstOnly",'16')

lblChampionParty = QtBind.createLabel(gui,'ChampionParty',21,182)
cbxAvoidChampionParty = QtBind.createCheckBox(gui,'cbxAvoidChampionParty_clicked','Avoid',80,182)
cbxOnlyChampionParty = QtBind.createCheckBox(gui,'cbxOnlyChampionParty_clicked','Only',150,182)
def cbxAvoidChampionParty_clicked(checked):
	Checkbox_Checked(checked,lstAvoid,"lstAvoid",'17') # 17 = ChampionParty
def cbxOnlyChampionParty_clicked(checked):
	Checkbox_Checked(checked,lstOnly,"lstOnly",'17')

lblGiantParty = QtBind.createLabel(gui,'GiantParty',21,201)
cbxAvoidGiantParty = QtBind.createCheckBox(gui,'cbxAvoidGiantParty_clicked','Avoid',80,201)
cbxOnlyGiantParty = QtBind.createCheckBox(gui,'cbxOnlyGiantParty_clicked','Only',150,201)
def cbxAvoidGiantParty_clicked(checked):
	Checkbox_Checked(checked,lstAvoid,"lstAvoid",'20') # 20 = GiantParty
def cbxOnlyGiantParty_clicked(checked):
	Checkbox_Checked(checked,lstOnly,"lstOnly",'20')

# Generalizing checkbox methods
def Checkbox_Checked(checked,lst,lstName,mobType):
	if checked:
		lst.append(mobType)
	else:
		lst.remove(mobType)
	saveConfig(lstName,lst)

# Return character configs path (JSON)
def getConfig():
	return get_config_dir()+pName+".json"

# Load default configs
def loadDefaultConfig():
	# Clear data
	QtBind.clear(gui,lstMobs)

# Load config if exists
def loadConfig():
	loadDefaultConfig()
	if os.path.exists(getConfig()):
		data = {}
		with open(getConfig(),"r") as f:
			data = json.load(f)
		# Check to load config
		if "lstMobs" in data:
			for d in data["lstMobs"]:
				QtBind.append(gui,lstMobs,d)
		if "lstAvoid" in data:
			lstAvoid = data["lstAvoid"]
			for i in range(len(lstAvoid)):
				if lstAvoid[i] == '8':
					QtBind.setChecked(gui,cbxAvoidUnique,True)
				elif lstAvoid[i] == '7':
					QtBind.setChecked(gui,cbxAvoidElite,True)
				elif lstAvoid[i] == '6':
					QtBind.setChecked(gui,cbxAvoidStrong,True)
				elif lstAvoid[i] == '5':
					QtBind.setChecked(gui,cbxAvoidTitan,True)
				elif lstAvoid[i] == '4':
					QtBind.setChecked(gui,cbxAvoidGiant,True)
				elif lstAvoid[i] == '1':
					QtBind.setChecked(gui,cbxAvoidChampion,True)
				elif lstAvoid[i] == '0':
					QtBind.setChecked(gui,cbxAvoidGeneral,True)
				elif lstAvoid[i] == '16':
					QtBind.setChecked(gui,cbxAvoidParty,True)
				elif lstAvoid[i] == '17':
					QtBind.setChecked(gui,cbxAvoidChampionParty,True)
				elif lstAvoid[i] == '20':
					QtBind.setChecked(gui,cbxAvoidGiantParty,True)
		if "lstOnly" in data:
			lstOnly = data["lstOnly"]
			for i in range(len(lstOnly)):
				if lstOnly[i] == '8':
					QtBind.setChecked(gui,cbxOnlyUnique,True)
				elif lstOnly[i] == '7':
					QtBind.setChecked(gui,cbxOnlyElite,True)
				elif lstOnly[i] == '6':
					QtBind.setChecked(gui,cbxOnlyStrong,True)
				elif lstOnly[i] == '5':
					QtBind.setChecked(gui,cbxOnlyTitan,True)
				elif lstOnly[i] == '4':
					QtBind.setChecked(gui,cbxOnlyGiant,True)
				elif lstOnly[i] == '1':
					QtBind.setChecked(gui,cbxOnlyChampion,True)
				elif lstOnly[i] == '0':
					QtBind.setChecked(gui,cbxOnlyGeneral,True)
				elif lstOnly[i] == '16':
					QtBind.setChecked(gui,cbxOnlyParty,True)
				elif lstOnly[i] == '17':
					QtBind.setChecked(gui,cbxOnlyChampionParty,True)
				elif lstOnly[i] == '20':
					QtBind.setChecked(gui,cbxOnlyGiantParty,True)

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
		log('Plugin: Mob added ['+text+']')

# Add mob to the list
def btnRemMob_clicked():
	selected = QtBind.text(gui,lstMobs)
	if selected and QtBind_ItemsContains(selected,lstMobs):
		QtBind.remove(gui,lstMobs,selected)
		saveConfig("lstMobs",QtBind.getItems(gui,lstMobs))
		log('Plugin: Mob removed ['+selected+']')

# Return True if text exist at the list
def ListContains(text,lst):
	for i in range(len(lst)):
		if lst[i].lower() == text.lower():
			return True
	return False

# Return True if item exists
def QtBind_ItemsContains(text,lst):
	return ListContains(text,QtBind.getItems(gui,lst))

# Attack all mobs around using the bot config. Ex: "AttackArea" or "AttackArea,5"
# Will be checking mobs every 5 seconds at the area as default.
def AttackArea(args):
	# stop bot and kill mobs through bot or continue script normally
	if getMobCount() > 0:
		# stop scripting
		stop_bot()
		# set automatically the training area
		p = get_position()
		set_training_position(p['region'], p['x'], p['y'])
		# waiting 5 seconds as default
		wait = 5
		if len(args) == 2:
			wait = float(args[1])
		# start to kill mobs on other thread because interpreter lock
		Timer(0.5,AttackMobs, (wait,False,p['x'],p['y'],p['z'])).start()
	# otherwise continue normally
	else:
		log("Plugin: Not mobs at this area.")
	return 0

# Attacking mobs using all configs from bot
def AttackMobs(wait,isAttacking,x,y,z):
	count = getMobCount()
	if count > 0:
		# Start to kill mobs using bot
		if isAttacking:
			log("Plugin: Killing ("+str(count)+") mobs at this area.")
		else:
			start_bot()
			log("Plugin: Starting to kill ("+str(count)+") mobs at this area.")
		# Check if there is not mobs to continue script
		Timer(wait,AttackMobs, (wait,True,x,y,z)).start()
	else:
		# All mobs killed, stop botting
		stop_bot()
		# Setting training area far away. The bot should continue where he was at the script
		set_training_position(0,0,0)
		# Move back to the starting point
		move_to(x,y,z)
		log("Plugin: All mobs killed.. Getting back to the script.")
		# give it some time to reach the movement
		Timer(2500,start_bot).start()

# Count all mobs around your character (60 or more it's the max. range I think)
def getMobCount():
	count = 0
	monsters = get_monsters()
	if monsters:
		for key, mob in monsters.items():
			# Avoid if this mob type is found
			if ListContains(str(mob['type']),lstAvoid):
				continue
			# Only count setup
			if len(lstOnly) > 0:
				# If is not in Only count, skip it
				if not ListContains(str(mob['type']),lstOnly):
					continue
			# Ignore mob names
			elif QtBind_ItemsContains(mob['name'],lstMobs):
				continue
			count+=1
	return count

# Plugin loading success
loadConfig()
log('Plugin: '+pName+' v'+pVersion+' succesfully loaded.')