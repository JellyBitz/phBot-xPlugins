from phBot import *
import urllib.request
import urllib.parse
import re

pName = 'xUpdater'
pVersion = '0.0.1'

# Check plugin version and update if is needed
def Check(currentVersion,url):
	with urllib.request.urlopen(url) as w:
		pyCode = str(w.read().decode("utf-8"))
		if re.search("pVersion = [0-9.'\"]*",pyCode):
			newVersion = re.search("pVersion = ([0-9.'\"]*)",pyCode)[1][1:-1]
			currentVersion= re.search("([0-9]*).([0-9]*).([0-9]*)",currentVersion)
			newVersion = re.search("([0-9]*).([0-9]*).([0-9]*)",newVersion)
			if int(newVersion[1]) > int(currentVersion[1]):
				pass
			elif int(newVersion[2]) > int(currentVersion[2]):
				pass
			elif int(newVersion[3]) > int(currentVersion[3]):
				pass
			else:
				return False
			pluginName = re.search('([a-zA-Z0-9]*).py',url)[1]
			log('Plugin: A new version ('+newVersion[1]+'.'+newVersion[2]+'.'+newVersion[3]+') is available!')
			with open(pluginName+'.py','w+') as f:
				f.write(pyCode)
			log('Plugin: Successfully updated! Try to reload the plugin')