from phBot import *
from threading import Timer
import QtBind
import struct
import json
import os

pName = 'xPackeTool'
pVersion = '0.1.2'
pUrl = 'https://raw.githubusercontent.com/JellyBitz/phBot-xPlugins/master/xPackeTool.py'

# Initializing GUI
gui = QtBind.init(__name__,pName)
lblInject = QtBind.createLabel(gui,'Inject Packets to Client/Server through bot, or just to parse what you need.',21,15)

cbxSro = QtBind.createCheckBox(gui, 'cbxSro_clicked','Show Client packets [C->S]',395,13)
cbxSro_checked = False
cbxJmx = QtBind.createCheckBox(gui, 'cbxJmx_clicked','Show Server packets [S->C]',560,13)
cbxJmx_checked = False

lblUsing = QtBind.createLabel(gui,'Opcode:\t              Data:',41,47)
txtOpcode = QtBind.createLineEdit(gui,"",85,45,40,20)
txtData = QtBind.createLineEdit(gui,"",163,45,450,20)
cbxEncrypted = QtBind.createCheckBox(gui, 'cbxEnc_clicked','Encrypted',620,47)
btnInjectPacket = QtBind.createButton(gui,'btnInjectPacket_clicked',"  Inject Packet  ",348,65)

cbxDontShow = QtBind.createCheckBox(gui, 'cbxDontShow_clicked',"Don't show",25,90)
cbxOnlyShow = QtBind.createCheckBox(gui, 'cbxOnlyShow_clicked',"Only Show",120,90)
QtBind.setChecked(gui,cbxDontShow,True) # using two checkbox like radiobutton
cbxDontShow_checked = True
lblOpcodes = QtBind.createLabel(gui,"The following list of opcodes ( Filter )",21,110)
tbxOpcodes = QtBind.createLineEdit(gui,"",21,129,100,20)
lstOpcodes = QtBind.createList(gui,21,151,176,109)
btnAddOpcode = QtBind.createButton(gui,'btnAddOpcode_clicked',"      Add      ",123,129)
btnRemOpcode = QtBind.createButton(gui,'btnRemOpcode_clicked',"     Remove     ",70,259)

# Checkbox "Show Client Packets" checked
def cbxSro_clicked(checked):
	global cbxSro_checked
	cbxSro_checked = checked

# Checkbox "Show Server Packets" checked
def cbxJmx_clicked(checked):
	global cbxJmx_checked
	cbxJmx_checked = checked

# Inject packet on button clicked
def btnInjectPacket_clicked():
	strOpcode = QtBind.text(gui,txtOpcode)
	strData = QtBind.text(gui,txtData)
	# Opcode or Data is not empty
	if strOpcode and strData:
		Packet = bytearray()
		opcode = int(strOpcode,16)
		data = strData.split()
		i = 0
		while i < len(data):
			Packet.append(int(data[i],16))
			i += 1
		encrypted = QtBind.isChecked(gui,cbxEncrypted)
		log("Plugin: Injecting packet ("+pName+")")
		inject_joymax(opcode,Packet,encrypted)

# Return plugin configs path (JSON)
def getConfig():
	return get_config_dir()+pName+".json"

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
	# init empty dictionary
	data = {}
	# load configs if exists
	if os.path.exists(getConfig()):
		with open(getConfig(),"r") as f:
			data = json.load(f)
	# Add or edit key for "DontShow" checkbox
	data["DontShow"] = checked
	# Replace configs
	with open(getConfig(),"w") as f:
		# Pretty-printing json :D
		f.write(json.dumps(data, indent=4, sort_keys=True))

# Load default configs
def loadDefaultConfig():
	# Clear data
	QtBind.clear(gui,lstOpcodes)

# Load the list of opcodes with the config file
def loadConfigs():
	loadDefaultConfig()
	if os.path.exists(getConfig()):
		data = {}
		with open(getConfig(),"r") as f:
			data = json.load(f)
		# load the opcodes list
		if "Opcodes" in data:
			for opcode in data["Opcodes"]:
				QtBind.append(gui,lstOpcodes,opcode)
		# config radiobutton if is saved
		if "DontShow" in data:
			global cbxDontShow_checked
			cbxDontShow_checked = data["DontShow"]
			QtBind.setChecked(gui,cbxDontShow,data["DontShow"])
			QtBind.setChecked(gui,cbxOnlyShow,not data["DontShow"])
		
# Return True if the opcode exists in the list
def lstOpcodes_exists(opcode):
	# parse to string for compare with all
	strOpcode = '0x{:02X}'.format(opcode)
	opcodes = QtBind.getItems(gui,lstOpcodes)
	for i in range(len(opcodes)):
		if opcodes[i] == strOpcode:
			return True
	return False
	
# Button "Add" clicked
def btnAddOpcode_clicked():
	# parse to HEX or fail trying
	opcode = int(QtBind.text(gui,tbxOpcodes),16)
	if opcode and not lstOpcodes_exists(opcode):
		data = {}
		if os.path.exists(getConfig()):
			with open(getConfig(),"r") as f:
				data = json.load(f)
		# Add or Create opcode into the list
		if "Opcodes" in data:
			data["Opcodes"].append('0x{:02X}'.format(opcode))
		else:
			data["Opcodes"] = ['0x{:02X}'.format(opcode)]
		with open(getConfig(),"w") as f:
			f.write(json.dumps(data, indent=4, sort_keys=True))
		QtBind.append(gui,lstOpcodes,'0x{:02X}'.format(opcode))
		# saved successfully
		QtBind.setText(gui, tbxOpcodes,"")
		log("Plugin: Added opcode [0x"+'{:02X}'.format(opcode)+"]")

# Button "Remove" clicked
def btnRemOpcode_clicked():
	selectedItem = QtBind.text(gui,lstOpcodes)
	if selectedItem:
		if os.path.exists(getConfig()):
			data = {}
			with open(getConfig(), 'r') as f:
				data = json.load(f)
			# try remove opcode from file loaded
			try:
				data["Opcodes"].remove(selectedItem)
				# Replace configs if selectedItem exists at least
				with open(getConfig(),"w") as f:
					f.write(json.dumps(data, indent=4, sort_keys=True))
			except:
				pass # just ignore file if don't exist
		QtBind.remove(gui,lstOpcodes,selectedItem)
		log("Plugin: Removed opcode ["+selectedItem+"]")

# return True if can log/show the packet
def show_packet(opcode):
	if lstOpcodes_exists(opcode):
		if not cbxDontShow_checked:
			return True
	elif cbxDontShow_checked:
		return True
	return False

# All packets received from Silkroad will be passed to this function
# Returning True will keep the packet and False will not forward it to the game server
def handle_silkroad(opcode, data):
	if cbxSro_checked:
		if show_packet(opcode):
			log("Client: (Opcode) 0x" + '{:02X}'.format(opcode) + " (Data) "+ ("None" if not data else ' '.join('{:02X}'.format(x) for x in data)))
	return True

# All packets received from Silkroad will be passed to this function
# Returning True will keep the packet and False will not forward it to the game server
def handle_joymax(opcode, data):
	if cbxJmx_checked:
		if show_packet(opcode):
			log("Server: (Opcode) 0x" + '{:02X}'.format(opcode) + " (Data) "+ ("None" if not data else ' '.join('{:02X}'.format(x) for x in data)))
	return True

# Load success
loadConfigs()
log('Plugin: '+pName+' v'+pVersion+' succesfully loaded')