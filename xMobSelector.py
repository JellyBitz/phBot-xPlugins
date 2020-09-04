from phBot import *
import QtBind
import struct
import json
import os

pName = 'xMobSelector'
pVersion = '1.0.0'
pUrl = 'https://raw.githubusercontent.com/JellyBitz/phBot-xPlugins/master/xMobSelector.py'

# ______________________________ Initializing ______________________________ #

# Globals
selectedUID = 0
isActived = False
isAutoRefresh = False
# Check if the version can show HP
showHP = tuple(map(int, (get_version().split(".")))) >= (23,8,5)

# Graphic user interface
gui = QtBind.init(__name__,pName)

lblMobs = QtBind.createLabel(gui,"* List of monsters near to you",6,10)
lstMobs = QtBind.createList(gui,6,30,510,229)
lstMobsData = []
btnRefreshMobs = QtBind.createButton(gui,'btnRefreshMobs_clicked',"   Refresh   ",6,259)
cbxAutoRefreshMobs = QtBind.createCheckBox(gui,'cbxAutoRefreshMobs_checked','Automatically',6+75,258)
btnAddMob = QtBind.createButton(gui,'btnAddMob_clicked',"  Add  ",6+510-75,259)

lblAutoSelectMobs = QtBind.createLabel(gui,"* Auto select mobs from this list",720-200,10)
lstAutoSelectMobs = QtBind.createList(gui,720-200,30,200,229)
lstAutoSelectMobsData = []
btnScanMobs = QtBind.createButton(gui,'btnScanMobs_clicked',"",720-84,259)
btnRemMob = QtBind.createButton(gui,'btnRemMob_clicked',"  Remove  ",720-200,259)

# ______________________________ Methods ______________________________ #

# Return character configs path (JSON)
def getConfig():
	return get_config_dir()+pName+ ".json"

# Load default configs
def loadDefaultConfig():
	# Clear data
	QtBind.setText(gui,btnScanMobs,"  Start Scanner  ")
	QtBind.clear(gui,lstMobs)
	QtBind.clear(gui,lstAutoSelectMobs)

# Save all config
def saveConfigs():
	# Save all data
	data = {}

	lstAutoSelect = []
	for mob in lstAutoSelectMobsData:
		lstAutoSelect.append({'name':mob['name'],'type':mob['type']});
	data["Mobs"] = lstAutoSelect

	# Override
	with open(getConfig(),"w") as f:
		f.write(json.dumps(data, indent=4, sort_keys=True))

# Loads all config previously saved
def loadConfigs():
	loadDefaultConfig()
	# Check config exists to load
	if os.path.exists(getConfig()):
		data = {}
		with open(getConfig(),"r") as f:
			data = json.load(f)
		# Load mob list
		if "Mobs" in data:
			global lstAutoSelectMobsData
			lstAutoSelectMobsData = data["Mobs"]
			for mob in data["Mobs"]:
				QtBind.append(gui,lstAutoSelectMobs,mob['name']+" ("+getMobType(mob['type'])+")")

# Gets the mob type text
def getMobType(t):
	if t == 0:
		return 'General'
	if t == 1:
		return 'Champion'
	if t == 4:
		return 'Giant'
	if t == 5:
		return 'Titan'
	if t == 6:
		return 'Strong'
	if t == 7:
		return 'Elite'
	if t == 8:
		return 'Unique'
	if t == 16:
		return 'Party General'
	if t == 17:
		return 'Party Champion'
	if t == 20:
		return 'Party Giant'
	return 'Unknown['+str(t)+']'

# Start/Stop scanning the mob list around
def btnScanMobs_clicked():
	global isActived
	if isActived:
		# Stop scanning
		isActived = False
		QtBind.setText(gui,btnScanMobs,"  Start Scanner  ")
	else:
		# Initialize value
		global selectedUID
		selectedUID = 0

		# Start scanning
		isActived = True
		QtBind.setText(gui,btnScanMobs,"  Stop Scanner  ")

# List of mobs actually around you
def btnRefreshMobs_clicked():
	# Clear the list
	QtBind.clear(gui,lstMobs)
	global lstMobsData
	lstMobsData = []

	# Get all mobs near to you
	mobs = get_monsters()
	if mobs:
		# add all kind of mobs actually found
		for uid, mob in mobs.items():
			# Add mob
			QtBind.append(gui,lstMobs,mob['name']+" ("+getMobType(mob['type'])+") "+(' - HP ('+str(mob['hp'])+'/'+str(mob['max_hp'])+')' if showHP else '')+" - UID ["+str(uid)+']')
			lstMobsData.append(mob)

# Check if is already on the selector list
def ListAutoSelectMob_Contains(mob):
	for _mob in lstAutoSelectMobsData:
		if _mob['name'] == mob['name'] and _mob['type'] == mob['type']:
			return True
	return False

# Add specific type of mobs to the selector list
def btnAddMob_clicked():
	# Selecting mob from the scan list
	selectedIndex = QtBind.currentIndex(gui,lstMobs)
	if selectedIndex >= 0:
		selectedMob = lstMobsData[selectedIndex]

		if not ListAutoSelectMob_Contains(selectedMob):
			QtBind.append(gui,lstAutoSelectMobs,selectedMob['name']+" ("+getMobType(selectedMob['type'])+")")

			global lstAutoSelectMobsData
			lstAutoSelectMobsData.append(selectedMob)
			saveConfigs()

# Remove mobs from the selector list
def btnRemMob_clicked():
	selectedIndex = QtBind.currentIndex(gui,lstAutoSelectMobs)
	if selectedIndex >= 0:
		QtBind.removeAt(gui,lstAutoSelectMobs,selectedIndex)

		global lstAutoSelectMobsData
		lstAutoSelectMobsData.pop(selectedIndex)
		saveConfigs()

# Checkbox event
def cbxAutoRefreshMobs_checked(checked):
	global isAutoRefresh
	isAutoRefresh = checked

# Scann mobs and target it if is required
def SearchAndDestroy():
	if len(lstAutoSelectMobsData) > 0:

		# Get nearby mobs
		mobs = get_monsters()

		global selectedUID
		# Check if mob died or gone far away
		if selectedUID:
			if mobs:
				for uid, mob in mobs.items():
					if uid == selectedUID:
						return
			selectedUID = 0

		# Check for a new target
		if mobs:
			for uid, mob in mobs.items():
				if ListAutoSelectMob_Contains(mob):
					Inject_SelectTarget(uid)
					return

# Inject Packet - Select Target
def Inject_SelectTarget(targetUID):
	packet = bytearray()
	packet = packet + struct.pack('<I',targetUID)
	inject_joymax(0x7045,packet, False)

# ______________________________ Events ______________________________ #

# All packets received from game server will be passed to this function
# Returning True will keep the packet and False will not forward it to the game client
def handle_joymax(opcode, data):
	if opcode == 0xB045 and isActived:
		global selectedUID
		# Check success
		if data[0] == 1:
			selectedUID = struct.unpack_from("<I",data,1)[0]
			log('Plugin: Selected UID ['+str(selectedUID)+']')
		else:
			selectedUID = 0

# Called every 500ms.
def event_loop():
	if isAutoRefresh:
		btnRefreshMobs_clicked()
	if isActived:
		SearchAndDestroy()

# Plugin load success
log('Plugin: '+pName+' v'+pVersion+' successfully loaded')

# Adding RELOAD plugin support
loadConfigs()