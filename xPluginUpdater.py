from phBot import *
import QtBind
import urllib.request
import re
import os
import shutil

pName = 'xPluginUpdater'
pVersion = '1.1.1'
pUrl = 'https://raw.githubusercontent.com/JellyBitz/phBot-xPlugins/master/xPluginUpdater.py'

# ______________________________ Initializing ______________________________ #

# Graphic user interface
gui = QtBind.init(__name__,pName)
lblPlugins = QtBind.createLabel(gui,"Plugins found from your folder",21,11)
lvwPlugins = QtBind.createList(gui,21,30,700,200)
lstPluginsData = []
btnCheck = QtBind.createButton(gui,'btnCheck_clicked',"  Check Updates  ",350,8)
btnUpdate = QtBind.createButton(gui,'btnUpdate_clicked',"  Update Plugin (Selected)  ",450,8)

# ______________________________ Methods ______________________________ #

# Get the plugins directory
def GetPluginsFolder():
	return str(os.path.dirname(os.path.realpath(__file__)))

# List and check all plugins from the same plugin folder
def btnCheck_clicked():
	QtBind.clear(gui,lvwPlugins)
	# List all files from Plugins folder
	pyFolder = GetPluginsFolder()
	files = os.listdir(pyFolder)
	# Load plugins data
	global lstPluginsData
	for filename in files:
		# Check only python files
		if filename.endswith(".py"):
			pyFile = pyFolder+"\\"+filename
			with open(pyFile,"r",errors='ignore') as f:
				pyCode = str(f.read())
				# Read file and check his version
				if re.search("\npVersion = [0-9a-zA-Z.'\"]*",pyCode):
					# Extract version
					pyVersion = re.search("\npVersion = ([0-9a-zA-Z.'\"]*)",pyCode).group(0)[13:-1]
					# Extract name if has one
					pyName = filename[:-3]
					if re.search("\npName = ([0-9a-zA-Z'\"]*)",pyCode):
						pyName = re.search("\npName = ([0-9a-zA-Z'\"]*)",pyCode).group(0)[10:-1]
					# Check if has url
					pyUrl = pyCode.find("\npUrl = ")
					# Show basic plugin info
					pyInfo = filename+" ("+pyName+" v"+pyVersion+") - "

					# Getting all required to update the plugin
					pData = {}
					pData['canUpdate'] = False
					# Save all data if has url
					if pyUrl != -1:
						# Extract the rest url, it's up to the plugin if the url is wrong :P
						pyUrl = pyCode[pyUrl+9:].split('\n')[0][:-1]
						pyNewVersion = getVersion(pyUrl)
						# Check if version is found and can be updated
						if pyNewVersion and compareVersion(pyVersion,pyNewVersion):
							# Save data to update
							pData['canUpdate'] = True
							pData['url'] = pyUrl
							pData['filename'] = filename
							pData['pName'] = pyName
							# Notify update
							pyInfo += "Update available (v"+pyNewVersion+")"
						else:
							pyInfo += "Updated"
					else:
						pyInfo += "Cannot be updated: URL not found"
					# Add info to GUi
					QtBind.append(gui,lvwPlugins,pyInfo)
					lstPluginsData.append(pData)

# Return version if can be found from hosted url
def getVersion(url):
	try:
		req = urllib.request.Request(url, headers={'User-Agent' : "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0"})
		with urllib.request.urlopen(req) as w:
			pyCode = str(w.read().decode("utf-8"))
			if re.search("\npVersion = [0-9.'\"]*",pyCode):
				return re.search("\npVersion = ([0-9a-zA-Z.'\"]*)",pyCode).group(0)[13:-1]
	except:
		pass
	return None

# return True if version A is lower than B
def compareVersion(a, b):
	# only numbers allowed
	a = tuple(map(int, (a.split("."))))
	b = tuple(map(int, (b.split("."))))
	return a < b

# Update plugin selected
def btnUpdate_clicked():
	# Get plugin selected
	indexSelected = QtBind.currentIndex(gui,lvwPlugins)
	if indexSelected >= 0:
		pyData = lstPluginsData[indexSelected]
		# Update plugin if can
		if "canUpdate" in pyData and pyData['canUpdate']:
			# Get url
			pyUrl = pyData['url']
			try:
				req = urllib.request.Request(pyUrl, headers={'User-Agent' : "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0"})
				with urllib.request.urlopen(req) as w:
					pyCode = str(w.read().decode("utf-8"))
					pyVersion = re.search("\npVersion = ([0-9a-zA-Z.'\"]*)",pyCode).group(0)[13:-1]
					# Create backup/copy
					pyFolder = GetPluginsFolder()+'\\'
					shutil.copyfile(pyFolder+pyData['filename'],pyFolder+pyData['pName']+".py.bkp")
					os.remove(pyFolder+pyData['filename'])
					# Create/Override file
					with open(pyFolder+pyData['pName']+".py","w+") as f:
						f.write(pyCode)
					# Update GUI
					QtBind.removeAt(gui,lvwPlugins,indexSelected)
					QtBind.append(gui,lvwPlugins,pyData['pName']+".py ("+pyData['pName']+" v"+pyVersion+") - Updated recently")
					log('Plugin: "'+pyData['pName']+'" plugin has been successfully updated')
			except:
				log("Plugin: Error updating your plugin. Try again later..")

# Plugin loaded
log('Plugin: '+pName+' v'+pVersion+' succesfully loaded')
