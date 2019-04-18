from phBot import *
import QtBind
from threading import Timer
import json
import os

pVersion = 'v0.1.3'
pName = 'xAutoDungeon'

# Initializing GUI
gui = QtBind.init(__name__,pName)

lblMobs = QtBind.createLabel(gui,'Add monster names to being ignored from the counter mobs.',21,11)
tbxMobs = QtBind.createLineEdit(gui,"",511,11,100,20)
lstMobs = QtBind.createList(gui,511,32,176,48)
btnAddMob = QtBind.createButton(gui,'btnAddMob_clicked',"    Add    ",612,10)
btnRemMob = QtBind.createButton(gui,'btnRemMob_clicked',"     Remove     ",560,79)

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
	if text and not lst_exist(text,lstMobs):
		QtBind.append(gui,lstMobs,text)
		QtBind.setText(gui,tbxMobs,"")
		saveConfig("lstMobs",QtBind.getItems(gui,lstMobs))
		log('Plugin: Mob added ['+text+']')

# Add mob to the list
def btnRemMob_clicked():
	selected = QtBind.text(gui,lstMobs)
	if selected and lst_exist(selected,lstMobs):
		QtBind.remove(gui,lstMobs,selected)
		saveConfig("lstMobs",QtBind.getItems(gui,lstMobs))
		log('Plugin: Mob removed ['+selected+']')

# Return True if text exist at the list
def lst_exist(text,lst):
	items = QtBind.getItems(gui,lst)
	for i in range(len(items)):
		if items[i].lower() == text.lower():
			return True
	return False

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
		Timer(0.5,AttackMobs, (wait,False)).start()
	# otherwise continue normally
	else:
		log("Plugin: Not mobs at this area.")
	return 0

# Attacking mobs using all configs from bot
def AttackMobs(wait,isAttacking):
	count = getMobCount()
	if count > 0:
		# Start to kill mobs using bot
		if isAttacking:
			log("Plugin: Killing ("+str(count)+") mobs at this area.")
		else:
			start_bot()
			log("Plugin: Starting to kill ("+str(count)+") mobs at this area.")
		# Check if there is not mobs to continue script
		Timer(wait,AttackMobs, (wait,True)).start()
	else:
		# All mobs killed, stop botting
		stop_bot()
		# Setting training area far away. The bot should continue where he was at the script
		set_training_position(0,0,0)
		log("Plugin: All mobs killed.. Getting back to the script.")
		Timer(0.5,start_bot).start()

# Count all mobs around your character (60 or more it's the max. range I think)
def getMobCount():
	count = 0
	monsters = get_monsters()
	if monsters:
		for key, mob in monsters.items():
			if lst_exist(mob["name"],lstMobs):
				continue
			count+=1
	return count

# Plugin loading success
loadConfig()
log('Plugin: '+pName+' '+pVersion+' succesfully loaded.')
# Check if module exists
try:
	import xUpdater
	xUpdater.Check(pVersion,'https://raw.githubusercontent.com/JellyBitz/phBot-xPlugins/master/'+pName+'.py')
except:
	pass