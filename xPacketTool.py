from phBot import *
import QtBind
import json
import os

pName = 'xPackeTool'
pVersion = '1.1.2'
pUrl = 'https://raw.githubusercontent.com/JellyBitz/phBot-xPlugins/master/xPackeTool.py'

# ______________________________ Initializing ______________________________ #

# Graphic user interface
gui = QtBind.init(__name__,pName)
lblInject = QtBind.createLabel(gui,'Inject Packets to Client/Server through bot, or analyze the packets you need.',6,10)

# Injection
_x=6
_y=50
lblOpcode = QtBind.createLabel(gui,'Opcode:',_x,_y)
txtOpcode = QtBind.createLineEdit(gui,"",_x+45,_y-3,32,20)
lblData = QtBind.createLabel(gui,'Data:',_x+45+32+6,_y)
txtData = QtBind.createLineEdit(gui,"",_x+45+32+6+32,_y-3,385,20)
cbxEncrypted = QtBind.createCheckBox(gui, 'cbxEnc_clicked','Encrypted',_x+432,_y-20)
_y+=25
btnInjectClient = QtBind.createButton(gui,'btnInjectClient_clicked',"  Inject To Client  ",_x+308,_y)
btnInjectServer = QtBind.createButton(gui,'btnInjectServer_clicked',"  Inject To Server  ",_x+404,_y)

# Filter
_x=720-176
_y=12
QtBind.createLineEdit(gui,"",_x-26,_y,1,265) # Separator line

cbxSro = QtBind.createCheckBox(gui, 'cbxShowClient_checked','Show Client packets [C->S]',_x+10,_y)
cbxShowClient = False
_y+=20
cbxJmx = QtBind.createCheckBox(gui, 'cbxShowServer_checked','Show Server packets [S->C]',_x+10,_y)
cbxShowServer = False

_y+=40
cbxDontShow = QtBind.createCheckBox(gui, 'cbxDontShow_clicked',"Don't show",_x+5,_y)
cbxOnlyShow = QtBind.createCheckBox(gui, 'cbxOnlyShow_clicked',"Only Show",_x+100,_y)
QtBind.setChecked(gui,cbxDontShow,True) # using two checkbox like radiobutton
cbxDontShow_checked = True
_y+=20
lblOpcodes = QtBind.createLabel(gui,"The following list of opcodes ( Filter )",_x,_y)
_y+=18
tbxOpcodes = QtBind.createLineEdit(gui,"",_x,_y,100,20)
btnAddOpcode = QtBind.createButton(gui,'btnAddOpcode_clicked',"      Add      ",_x+100+2,_y-2)
_y+=20
lstOpcodes = QtBind.createList(gui,_x,_y,176,120)
lstOpcodesData = []
btnRemOpcode = QtBind.createButton(gui,'btnRemOpcode_clicked',"     Remove     ",_x+88-32,_y-1+120)

# ______________________________ Methods ______________________________ #

# Return plugin configs path (JSON)
def getConfig():
	return get_config_dir()+pName+".json"

# Load default configs
def loadDefaultConfig():
	# Clear data
	global lstOpcodesData
	lstOpcodesData = []

	QtBind.clear(gui,lstOpcodes)

# Load the list of opcodes with the config file
def loadConfigs():
	loadDefaultConfig()
	if os.path.exists(getConfig()):
		data = {}
		with open(getConfig(),"r") as f:
			data = json.load(f)
		# load the opcodes list
		if "FilteredOpcodes" in data:
			global lstOpcodesData
			lstOpcodesData = data["FilteredOpcodes"]
			for opcode in lstOpcodesData:
				QtBind.append(gui,lstOpcodes,'0x{:02X}'.format(opcode))
		# config radiobutton if is saved
		if "DontShow" in data:
			global cbxDontShow_checked
			cbxDontShow_checked = data["DontShow"]
			QtBind.setChecked(gui,cbxDontShow,data["DontShow"])
			QtBind.setChecked(gui,cbxOnlyShow,not data["DontShow"])
		
# Save all config
def saveConfigs():
	# Save all data
	data = {}
	data['DontShow'] = cbxDontShow_checked
	data['FilteredOpcodes'] = lstOpcodesData

	# Overrides
	with open(getConfig(),"w") as f:
		f.write(json.dumps(data, indent=4, sort_keys=True))

# Checkbox "Show Client Packets" checked
def cbxShowClient_checked(checked):
	global cbxShowClient
	cbxShowClient = checked

# Checkbox "Show Server Packets" checked
def cbxShowServer_checked(checked):
	global cbxShowServer
	cbxShowServer = checked

# Inject packet on button clicked
def btnInjectServer_clicked():
	btnInjectPacket(inject_joymax)

# Inject packet on button clicked
def btnInjectClient_clicked():
	btnInjectPacket(inject_silkroad)

# Inject packet to the direction specified
def btnInjectPacket(IProxySend):
	strOpcode = QtBind.text(gui,txtOpcode)
	strData = QtBind.text(gui,txtData)
	# Opcode or Data is not empty
	if strOpcode and strData:
		data = bytearray()
		opcode = int(strOpcode,16)
		strData = strData.split()
		i = 0
		while i < len(data):
			data.append(int(strData[i],16))
			i += 1
		encrypted = QtBind.isChecked(gui,cbxEncrypted)
		# Show injection log
		log("Plugin: Injecting packet"+(' (Encrypted)' if encrypted else '')+" :")
		log("(Opcode) 0x" + '{:02X}'.format(opcode) + " (Data) "+ ("None" if not data else ' '.join('{:02X}'.format(x) for x in data)))
		IProxySend(opcode,data,encrypted)

# Checkbox "Don't show" checked
def cbxDontShow_clicked(checked):
	cbxDontShow_editConfig(checked)
	QtBind.setChecked(gui,cbxOnlyShow,not checked)
	
# Checkbox "Only Show" checked
def cbxOnlyShow_clicked(checked):
	cbxDontShow_editConfig(not checked)
	QtBind.setChecked(gui,cbxDontShow,not checked)

# Edit Key "DontShow" into the config file
def	cbxDontShow_editConfig(checked):
	global cbxDontShow_checked
	cbxDontShow_checked = checked
	saveConfigs()
	
# Button "Add" clicked
def btnAddOpcode_clicked():
	# Avoid empty data
	opcode = QtBind.text(gui,tbxOpcodes)
	if not opcode:
		return
	# Try to normalize it
	try:
		opcode = int(opcode,16)
	except Exception as ex:
		log("Plugin: Error ["+str(ex)+"]")
		return
	# Check if is already added
	global lstOpcodesData
	if not opcode in lstOpcodesData:
		lstOpcodesData.append(opcode)
		strOpcode = '0x{:02X}'.format(opcode)
		QtBind.append(gui,lstOpcodes,strOpcode)
		saveConfigs()
		# saved successfully
		QtBind.setText(gui, tbxOpcodes,"")
		log("Plugin: Added opcode ["+strOpcode+"]")

# Button "Remove" clicked
def btnRemOpcode_clicked():
	selectedIndex = QtBind.currentIndex(gui,lstOpcodes)
	if selectedIndex >= 0:
		strOpcode = '0x{:02X}'.format(lstOpcodesData[selectedIndex])
		del lstOpcodesData[selectedIndex]
		QtBind.removeAt(gui,lstOpcodes,selectedIndex)
		# saved successfully
		saveConfigs()
		log("Plugin: Removed opcode ["+strOpcode+"]")

# return True if can log/show the packet
def CanShowPacket(opcode):
	if opcode in lstOpcodesData:
		if not cbxDontShow_checked:
			return True
	elif cbxDontShow_checked:
		return True
	return False

# ______________________________ Events ______________________________ #

# Inject packet through Script. All his data is separated by comma, encrypted will be false if it's not specified.
# Example 1: "inject,Opcode,ItsEncrypted?,Data?,Data?,Data?,..."
# Example 2: "inject,3091,False,0" or "inject,3091,0" (which means greet action)
def inject(args):
	argCount = len(args)
	if argCount < 2:
		log("Plugin: Incorrect structure to inject packet")
		return 0
	# Check packet structure
	opcode = int(args[1],16)
	data = bytearray()
	encrypted = False
	dataIndex = 2
	if argCount >= 3:
		enc = args[2].lower()
		if enc == 'true' or enc == 'false':
			encrypted = enc == "true"
			dataIndex +=1
	# Create packet data and inject it
	for i in range(dataIndex, argCount):
		data.append(int(args[i],16))
	# Show injection log
	log("Plugin: Injecting packet"+(' (Encrypted)' if encrypted else '')+" :")
	log("(Opcode) 0x" + '{:02X}'.format(opcode) + " (Data) "+ ("None" if not data else ' '.join('{:02X}'.format(x) for x in data)))
	# inject it
	inject_joymax(opcode,data,encrypted)
	return 0

# All packets received from Silkroad will be passed to this function
# Returning True will keep the packet and False will not forward it to the game server
def handle_silkroad(opcode, data):
	if cbxShowClient:
		if CanShowPacket(opcode):
			log("Client: (Opcode) 0x" + '{:02X}'.format(opcode) + " (Data) "+ ("None" if not data else ' '.join('{:02X}'.format(x) for x in data)))
	return True

# All packets received from game server will be passed to this function
# Returning True will keep the packet and False will not forward it to the game client
def handle_joymax(opcode, data):
	if cbxShowServer:
		if CanShowPacket(opcode):
			log("Server: (Opcode) 0x" + '{:02X}'.format(opcode) + " (Data) "+ ("None" if not data else ' '.join('{:02X}'.format(x) for x in data)))
	return True

# Plugin loaded
log('Plugin: '+pName+' v'+pVersion+' succesfully loaded')
loadConfigs()
