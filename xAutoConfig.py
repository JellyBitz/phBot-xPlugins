from phBot import *
import shutil
import os

pName = 'xAutoConfig'
pVersion = '0.2.1'
pUrl = 'https://raw.githubusercontent.com/JellyBitz/phBot-xPlugins/master/xAutoConfig.py'

# Called when the user successfully selects a character. No character data has been loaded yet.
def joined_game():
	# JSON config not found
	if not os.path.exists(get_config_path()):
		# JSON default configs path
		defaultConfig = get_config_dir()+"Default.json"
		if os.path.exists(defaultConfig):
			shutil.copyfile(defaultConfig,get_config_path())
			log("Plugin: Default JSON loaded")
		# db3 default filter path
		defaultFilter = get_config_dir()+"Default.db3"
		if os.path.exists(defaultFilter):
			shutil.copyfile(defaultFilter,get_config_path().replace(".json",".db3"))
			log("Plugin: Default Filter loaded")

log('Plugin: '+pName+' v'+pVersion+' successfully loaded')