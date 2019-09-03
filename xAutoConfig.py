from phBot import *
from threading import Timer
import shutil
import os

pName = 'xAutoConfig'
pVersion = '0.2.3'
pUrl = 'https://raw.githubusercontent.com/JellyBitz/phBot-xPlugins/master/xAutoConfig.py'

# Called when the user successfully selects a character. No character data has been loaded yet.
def joined_game():
	# JSON config check
	if not os.path.exists(get_config_path()):
		# JSON default configs path
		ReplaceConfig(get_config_dir()+"Default.json",get_config_path(),"Plugin: Default JSON loaded")
		# db3 default filter path
		Timer(10.0,ReplaceConfig,(get_config_dir()+"Default.db3",get_config_path().replace(".json",".db3"),"Plugin: Default Filter loaded"),).start()

def ReplaceConfig(newPath,oldPath,message):
	if os.path.exists(newPath):
		shutil.copyfile(newPath,oldPath)
		log(message)

log('Plugin: '+pName+' v'+pVersion+' successfully loaded')