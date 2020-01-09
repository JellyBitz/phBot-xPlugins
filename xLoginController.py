from phBot import *
import QtBind
import json
import os
from datetime import timedelta
from datetime import datetime
from threading import Timer

pName = 'xLoginController'
pVersion = '0.0.3'
pUrl = 'https://raw.githubusercontent.com/JellyBitz/phBot-xPlugins/master/xLoginController.py'

# Globals
timerCheck = None
character_data = None

# Initializing GUI
gui = QtBind.init(__name__,pName)
cbxEnabled = QtBind.createCheckBox(gui,'checkbox_clicked','Enable '+pName+' plugin',21,13)

lblFromTime = QtBind.createLabel(gui,"FROM",21,45)
strFromTime = "00:00"
tbxFromTime = QtBind.createLineEdit(gui,strFromTime,55,43,37,20)

lblToTime = QtBind.createLabel(gui,"TO",101,45)
strToTime = "23:59"
tbxToTime = QtBind.createLineEdit(gui,strToTime,121,43,37,20)
btnSaveTimes = QtBind.createButton(gui,'btnSaveTimes_clicked',"  Save  ",165,43)

# Return folder path
def getPath():
	return get_config_dir()+pName+"\\"

# Return character configs path (JSON)
def getConfig():
	return getPath()+character_data["server"]+"_"+character_data["name"]+".json"

# Load default configs
def loadDefaultConfig():
	# Clear data
	QtBind.setChecked(gui,cbxEnabled,False)
	strFromTime = "00:00"
	QtBind.setText(gui, tbxFromTime,strFromTime)
	strToTime = "23:59"
	QtBind.setText(gui, tbxToTime,strToTime)

# Load config if exists
def loadConfig():
	loadDefaultConfig()
	if os.path.exists(getConfig()):
		data = {}
		with open(getConfig(),"r") as f:
			data = json.load(f)
		# Check to load config
		if "FROM" in data:
			global strFromTime
			strFromTime = data["FROM"]
			QtBind.setText(gui,tbxFromTime,strFromTime)
		if "TO" in data:
			global strToTime
			strToTime = data["TO"]
			QtBind.setText(gui,tbxToTime,strToTime)
		if "Enabled" in data:
			QtBind.setChecked(gui,cbxEnabled,data["Enabled"])
			# Check to start running the timer checker
			if data["Enabled"]:
				CheckTimer()
		else:
			QtBind.setChecked(gui,cbxEnabled,False)

# Called when the character enters the game world
def joined_game():
	global character_data
	character_data = get_character_data()
	loadConfig()

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

# Just saving everything about checkboxs everytime
def checkbox_clicked(checked):
	if character_data:
		enabled = QtBind.isChecked(gui,cbxEnabled)
		saveConfig("Enabled",enabled)
		# activate/deactivate timer inmediatly
		if enabled:
			CheckTimer()
			log('Plugin: '+pName+' has been enabled')	
		else:
			StopTimer()
			log('Plugin: '+pName+' has been disabled')

# Save times on button clicked
def btnSaveTimes_clicked():
	if character_data:
		tempFromTime = None
		tempToTime = None
		try:
			tempFromTime = QtBind.text(gui,tbxFromTime)
			tempFromTime = datetime.strptime(tempFromTime, '%H:%M')
		except:
			log('Plugin: Error! FROM time needs to be at format "00:00" (hh:mm)')
			return
		try:
			tempToTime = QtBind.text(gui,tbxToTime)
			tempToTime = datetime.strptime(tempToTime, '%H:%M')
		except:
			log('Plugin: Error! TO time needs to be at format "00:00" (hh:mm)')
			return
		if tempFromTime == tempToTime:
			log('Plugin: Error! times cannot be equal, a better option is to disable the plugin')
			return
		# Everything is right..
		global strFromTime,strToTime
		strFromTime = tempFromTime.strftime('%H:%M')
		strToTime = tempToTime.strftime('%H:%M')
		saveConfig("FROM",strFromTime)
		saveConfig("TO",strToTime)
		log("Plugin: Times saved correctly!")

def CheckTimer():
	timeNow = datetime.now()
	
	timeFrom = datetime(timeNow.year, timeNow.month, timeNow.day, int(strFromTime.split(':')[0]), int(strFromTime.split(':')[1]), 0)
	timeTo = datetime(timeNow.year, timeNow.month, timeNow.day, int(strToTime.split(':')[0]), int(strToTime.split(':')[1]), 0)
	# Add 1 day to fix interval
	if timeFrom > timeTo:
		timeTo += timedelta(days=1)

	if timeNow >= timeFrom and timeNow <= timeTo:
		reconnect(True)
	else:
		stop_bot()
		reconnect(False)
		disconnect()

	# Check every 30 seconds
	RestartCheckTimer(30.0)

def StopTimer():
	global timerCheck
	if timerCheck:
		timerCheck.cancel()
		timerCheck = None

def RestartCheckTimer(interval):
	global timerCheck
	if timerCheck:
		timerCheck.cancel()
	timerCheck = Timer(interval,CheckTimer)
	timerCheck.start()

# Plugin loaded success
log("Plugin: "+pName+" v"+pVersion+" successfully loaded")
# Creating configs folder
if not os.path.exists(getPath()):
	os.makedirs(getPath())
	log('Plugin: '+pName+' folder has been created')

# You'll have to start login all bots you want to use for the account.

# The config times (FROM -> TO) at formats 00:00-23:59 (HH:MM) needs to be saved by characters at least once
# otherwise the plugin will be disabled as default.

# You can choose intervals like "FROM 23:59 TO 00:01" that should work with no problem.
# START BOT ON LOGIN is already implemented on phbot so you could use that.
# RELOG ON DISCONNECT is handled by plugin, you can check it through bot, it doesn't matter.

# You cannot use button RELOAD from Plugins for a few reasons
# as example if you do it while this plugin is working or phbot will crash..