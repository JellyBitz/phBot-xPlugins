from phBot import *
import urllib.request
import urllib.parse
import re

pName = 'xPluginUpdater'
pVersion = '0.0.2'

# Check plugin version and update if is needed. Return True if has been updated
# If plugin name is not specified, it will try to take from url
def Check(currentVersion,url,name=None):
	try:
		req = urllib.request.Request(url, headers={'User-Agent' : "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0"})
		with urllib.request.urlopen(req) as w:
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
				if not name:
					name = re.search('/([a-zA-Z0-9]*).py',url)[1]
				log('Plugin: A new version ('+newVersion[1]+'.'+newVersion[2]+'.'+newVersion[3]+') is available!')
				with open(name+'.py','w+') as f:
					f.write(pyCode)
				log('Plugin: Successfully updated! Try to reload the plugin')
				return True
	except:
		pass
	return False

# Load success
log('Plugin: '+pName+' v'+pVersion+' succesfully loaded.')
Check(pVersion,'https://raw.githubusercontent.com/JellyBitz/phBot-xPlugins/master/'+pName+'.py')