from phBot import *
import QtBind

pVersion = 'v0.1.0'
pName = 'xNPC'
pUrl = 'https://raw.githubusercontent.com/JellyBitz/phBot-xPlugins/master/xNPC.py'

# Needed for phbot GUI
gui = QtBind.init(__name__,pName)
lblNpcs = QtBind.createLabel(gui,"List of NPC's near to you..",21,11)
btnNpcs = QtBind.createButton(gui,'btnNpcs_clicked',"  Refresh list  ",645,8)
lstNpcs = QtBind.createList(gui,21,30,700,200)

# Clear and load the list of NPCs		
def btnNpcs_clicked():
	# Get all NPCs and teleporters
	npcs = get_npcs()
	# Clear list
	QtBind.clear(gui,lstNpcs)
	# Add header
	QtBind.append(gui,lstNpcs,'[Name] [ServerName] [ModelID] (UniqueID)')
	if npcs:
		# Header data separation
		QtBind.append(gui,lstNpcs,' -')
		for UniqueID, NPC in npcs.items():
			# Append every NPC description to the list
			QtBind.append(gui,lstNpcs,"["+NPC['name'] + "] ["+NPC['servername']+"] ["+str(NPC['model'])+"] ("+str(UniqueID)+")")

log('Plugin: '+pName+' '+pVersion+' successfully loaded.')