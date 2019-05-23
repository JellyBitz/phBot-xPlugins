from phBot import *
import phBotChat
import QtBind
import os
from threading import Timer
import urllib.request

pName = 'xKervanKey'
pVersion = '0.1.0'

# SET YOUR CUSTOM "xkervankey.txt" PATH HERE.
# xkervankey_path = r"C:\Users\MyUser\Downloads\phBot\Plugins\xkervankey.txt" # EXAMPLE
xkervankey_path = ""

# Initializing GUI
gui = QtBind.init(__name__,pName)
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
	# Emulating a quick browser to open the site
	req = urllib.request.Request("https://www.joysro.net/code.php", headers={'User-Agent' : "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0"})
	# Getting stream
	resp = urllib.request.urlopen(req)
	# Getting data
	html = str(resp.read().decode("utf-8"))
	# Extracting data
	searchingStart = '<h1>'
	searchingEnd = '</h1>'
	index = html.find(searchingStart)
	if index != -1:
		return html[index+len(searchingStart):].split(searchingEnd)[0]
	return ""

# All chat messages received are sent to this function
def handle_chat(t, player, msg):
	if player:
		if player == "JOYCONTROL" and "joysro.net" in msg:
			Timer(1.0,phBotChat.Private,(player,getKervanKey())).start()

# Success at loading
log("Plugin: "+pName+" v"+pVersion+" [JOYSRO] successfully loaded")
getKervanKey() # Just for testing purpose