from phBot import *
import QtBind
import urllib.request
import re
import os

pName = 'xPluginUpdater'
pVersion = '0.1.1'
pUrl = 'https://raw.githubusercontent.com/JellyBitz/phBot-xPlugins/master/xPluginUpdater.py'

# Initializing GUI
gui = QtBind.init(__name__,pName)
lblPlugins = QtBind.createLabel(gui,"Plugins found from your folder",21,11)
lstPlugins = QtBind.createList(gui,21,30,700,200)
btnCheck = QtBind.createButton(gui,'btnCheck_clicked',"  Check Updates  ",350,8)
btnUpdate = QtBind.createButton(gui,'btnUpdate_clicked',"  Update Plugin (Selected)  ",450,8)

def GetPluginsFolder():
	return str(os.path.dirname(os.path.realpath(__file__)))

# List and check all plugins from the same plugin folder
def btnCheck_clicked():
	QtBind.clear(gui,lstPlugins)
	# List all files from Plugins folder
	files = os.listdir(GetPluginsFolder())
	for filename in files:
		# Check only python files
		if(re.search("[.]py",filename)):
			pyFile = GetPluginsFolder()+"\\"+filename
			with open(pyFile,"r") as f:
				pyCode = str(f.read())
				# Read file and check his version
				if re.search("\npVersion = [0-9a-zA-Z.'\"]*",pyCode):
					pyVersion = re.search("\npVersion = ([0-9a-zA-Z.'\"]*)",pyCode).group(0)[1:-1]
					pyName = re.search("\npName = ([0-9a-zA-Z'\"]*)",pyCode).group(0)[1:-1]
					pyDesc = pyVersion
					if pyName and pyName+".py" != filename:
						pyDesc = pyName+" "+pyDesc
					# It's up to the plugin if the url is wrong :P
					pyUrl = pyCode.find("\npUrl = ")
					pyMsg = "Updated"
					if pyUrl != -1:
						pyUrl = pyCode[pyUrl+9:].split('\n')[0][:-1]
						pyNewVersion = getVersion(pyUrl)
						if pyNewVersion and compareVersion(pyVersion,pyNewVersion):
							pyMsg = "Update available (v"+pyNewVersion+") ["+pyUrl+"]"
					else:
						pyMsg = "Cannot be update: URL not found"
					QtBind.append(gui,lstPlugins,filename+" ("+pyDesc+") - "+pyMsg)

# Return version if can be found from hosted url
def getVersion(url):
	try:
		req = urllib.request.Request(url, headers={'User-Agent' : "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0"})
		with urllib.request.urlopen(req) as w:
			pyCode = str(w.read().decode("utf-8"))
			if re.search("\npVersion = [0-9.'\"]*",pyCode):
				return re.search("\npVersion = ([0-9a-zA-Z.'\"]*)",pyCode).group(0)[1:-1]
	except:
		pass
	return None

# return True if version A is lower than B
def compareVersion(a, b):
	va = a.split('.')
	vb = b.split('.')
	if va != 1 and vb != 1:
		# force update: version format has changed
		if len(va) != len(vb):
			return True
		# Check only numbers
		# (letters are ignored, considered as beta)
		for i in range(len(va)):
			numA = re.search("(\d*)",va[i]).group(0)
			numB = re.search("(\d*)",vb[i]).group(0)
			if numA < numB:
				return True
	return False

# Update plugin selected
def btnUpdate_clicked():
	py = QtBind.text(gui,lstPlugins)
	if py and "- Update available" in py:
		# Get url from GUI
		pyUrl = py[py.find('[')+1:py.find(']')]
		try:
			req = urllib.request.Request(pyUrl, headers={'User-Agent' : "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0"})
			with urllib.request.urlopen(req) as w:
				pyCode = str(w.read().decode("utf-8"))
				filename = py[:py.find(' ')]
				with open(filename+"a","w+") as f:
					f.write(pyCode)
				QtBind.remove(gui,lstPlugins,py)
				pyVersion = py[py.rfind('(')+1:py.rfind(')')]
				QtBind.append(gui,lstPlugins,filename+" ("+pyVersion+") - Updated recently")
				log('Plugin: Your plugin has been successfully updated')
		except:
			log("Plugin: Error updating your plugin. Try again later..")

# Load success
log('Plugin: '+pName+' v'+pVersion+' succesfully loaded')