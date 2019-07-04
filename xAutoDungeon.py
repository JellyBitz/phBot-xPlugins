from phBot import *
import QtBind
from threading import Timer
import json
import os

pVersion = '0.3.1'
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
	if checked:
		lstAvoid.append('8') # 8 = Unique
	else:
		lstAvoid.remove('8')
	saveConfig("lstAvoid",lstAvoid)
def cbxOnlyUnique_clicked(checked):
	if checked:
		lstOnly.append('8')
	else:
		lstOnly.remove('8')
	saveConfig("lstOnly",lstOnly)

lblElite = QtBind.createLabel(gui,'Elite',21,49)
cbxAvoidElite = QtBind.createCheckBox(gui,'cbxAvoidElite_clicked','Avoid',80,49)
cbxOnlyElite = QtBind.createCheckBox(gui,'cbxOnlyElite_clicked','Only',150,49)
def cbxAvoidElite_clicked(checked):
	if checked:
		lstAvoid.append('7') # 7 = Elite
	else:
		lstAvoid.remove('7')
	saveConfig("lstAvoid",lstAvoid)
def cbxOnlyElite_clicked(checked):
	if checked:
		lstOnly.append('7')
	else:
		lstOnly.remove('7')
	saveConfig("lstOnly",lstOnly)

lblStrong = QtBind.createLabel(gui,'Strong',21,68)
cbxAvoidStrong = QtBind.createCheckBox(gui,'cbxAvoidStrong_clicked','Avoid',80,68)
cbxOnlyStrong = QtBind.createCheckBox(gui,'cbxOnlyStrong_clicked','Only',150,68)
def cbxAvoidStrong_clicked(checked):
	if checked:
		lstAvoid.append('6') # 6 = Strong
	else:
		lstAvoid.remove('6')
	saveConfig("lstAvoid",lstAvoid)
def cbxOnlyStrong_clicked(checked):
	if checked:
		lstOnly.append('6')
	else:
		lstOnly.remove('6')
	saveConfig("lstOnly",lstOnly)

lblTitan = QtBind.createLabel(gui,'Titan',21,87)
cbxAvoidTitan = QtBind.createCheckBox(gui,'cbxAvoidTitan_clicked','Avoid',80,87)
cbxOnlyTitan = QtBind.createCheckBox(gui,'cbxOnlyTitan_clicked','Only',150,87)
def cbxAvoidTitan_clicked(checked):
	if checked:
		lstAvoid.append('5') # 5 = Titan
	else:
		lstAvoid.remove('5')
	saveConfig("lstAvoid",lstAvoid)
def cbxOnlyTitan_clicked(checked):
	if checked:
		lstOnly.append('5')
	else:
		lstOnly.remove('5')
	saveConfig("lstOnly",lstOnly)

lblGiant = QtBind.createLabel(gui,'Giant',21,87)
cbxAvoidGiant = QtBind.createCheckBox(gui,'cbxAvoidGiant_clicked','Avoid',80,87)
cbxOnlyGiant = QtBind.createCheckBox(gui,'cbxOnlyGiant_clicked','Only',150,87)
def cbxAvoidGiant_clicked(checked):
	if checked:
		lstAvoid.append('4') # 4 = Giant
	else:
		lstAvoid.remove('4')
	saveConfig("lstAvoid",lstAvoid)
def cbxOnlyGiant_clicked(checked):
	if checked:
		lstOnly.append('4')
	else:
		lstOnly.remove('4')
	saveConfig("lstOnly",lstOnly)

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