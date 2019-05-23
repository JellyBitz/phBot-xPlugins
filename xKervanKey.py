from phBot import *
import phBotChat
import QtBind
import os
from time import sleep
import urllib.request

# SET YOUR CUSTOM "xkervankey.txt" PATH HERE.
# xkervankey_path = r"C:\Users\MyUser\Downloads\phBot\Plugins\xkervankey.txt" # EXAMPLE
xkervankey_path = ""

# Initializing GUI
gui = QtBind.init(__name__,'xKervanKey')
lblKey = QtBind.createLabel(gui,"KervanKey:",21,11)
tbxKey = QtBind.createLineEdit(gui,"",130,12,150,18)
btnKey = QtBind.createButton(gui, "btnKey_clicked","Save",300,11)

# Return kervankey file path
def getKervanKeyPath():
	if xkervankey_path:
		return xkervankey_path;
	return os.path.dirname(os.path.realpath(__file__))+"\\xkervankey.txt"

# Save the kervankey from phBot GUI to update all bots
def btnKey_clicked():
	key = QtBind.text(gui,tbxKey)
	if key:
		with open(getKervanKeyPath(), "w") as f:
			f.write(key.strip())

# Load kervankey from file if exists, return result
def loadKervanKey():
	# Reading key from file
	key = ""
	if os.path.exists(getKervanKeyPath()):
		with open(getKervanKeyPath(),"r") as f:
			key = f.read()
		# Update if file is not empty
		if key:
			QtBind.setText(gui, tbxKey,key)
	# Load from GUI
	key = QtBind.text(gui,tbxKey)
	return key

# Return string containing the kervankey
def getKervanKey():
	# Getting KervanKey from GUI
	key = loadKervanKey()
	# Try to get KervanKey from url
	if not key:
		key = loadKervanKeyFromSite()
	# Checking success through phBot 
	if key:
		log("Plugin: KervanKey has been extracted ["+key+"]")
	else:
		log("Plugin: KervanKey not found")
	return key

# Load website to extract the key
def loadKervanKeyFromSite():
	# Emulating a quick browser to open google docs
	req = urllib.request.Request("https://docs.google.com/spreadsheets/d/1xhbP2qcBLscZ7j8D14QqkS44MU1kEkOQZqh24kwdfXQ/export?format=csv", headers={'User-Agent' : "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0"})
	# Getting stream
	resp = urllib.request.urlopen(req)
	# Getting data
	html = str(resp.read().decode("utf-8"))
	# Extracting data from excel (CSV format)
	index = html.find(',RSilkroad - KervanKey :,,,,')
	if index != -1:
		return html[index+28:].split(",")[0]
	return ""

# All chat messages received are sent to this function
def handle_chat(t, player, msg):
	if player:
		if player == "BotCheck" and "BotCheck" in msg:
			sleep(1.0)
			phBotChat.Private(player,getKervanKey())

# Success at loading
log("Plugin: xKervanKey v0.0.10 successfully loaded.")
getKervanKey() # Just for testing purpose