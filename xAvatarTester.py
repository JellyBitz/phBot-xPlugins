from phBot import *
import QtBind
from threading import Thread
from threading import Timer
import struct
import sqlite3
import json
import os

pName = 'xAvatarTester'
pVersion = '1.0.1'
pUrl = 'https://raw.githubusercontent.com/JellyBitz/phBot-xPlugins/master/xAvatarTester.py'

# ______________________________ Initializing ______________________________ #

bot_path = os.getcwd()
character_data = None
avatarTestingUID_MIN = 777777777
avatarTestingUID = 0
threadSearching = None

# Graphic user interface
gui = QtBind.init(__name__,pName)


# Search
_y = 12
_x = 6
lblSearchItem = QtBind.createLabel(gui,"Item name :",_x,_y)
tbxSearchItem = QtBind.createLineEdit(gui,"",_x+63,_y-3,568,20)
btnSearchItem = QtBind.createButton(gui,'btnSearchItem_clicked',"     Search     ",_x+63+568+3,_y-5)
_y+=22
lvwItems = QtBind.createList(gui,_x,_y,720-12,106)
lvwItemsData = []
_y+=106
btnAddItem = QtBind.createButton(gui,'btnAddItem_clicked',"     Add     ",_x,_y+3)

# Builder
_x+=90
_y+=10
lblHatItems = QtBind.createLabel(gui,"* Hat",_x,_y)
lblDressItems = QtBind.createLabel(gui,"* Dress",_x+152+3,_y)
lblAccesoryItems = QtBind.createLabel(gui,"* Accesory",_x+152+3+152+3,_y)
lblFlagItems = QtBind.createLabel(gui,"* Flag",_x+152+3+152+3+152+3,_y)
_y+=18
lvwHatItems = QtBind.createList(gui,_x,_y,152,80)
lvwHatItemsData = []
lvwDressItems = QtBind.createList(gui,_x+152+3,_y,152,80)
lvwDressItemsData = []
lvwAccesoryItems = QtBind.createList(gui,_x+152+3+152+3,_y,152,80)
lvwAccesoryItemsData = []
lvwFlagItems = QtBind.createList(gui,_x+152+3+152+3+152+3,_y,152,80)
lvwFlagItemsData = []
_y+=80
btnRemHatItem = QtBind.createButton(gui,'btnRemHatItem_clicked',"     Remove     ",_x+36,_y)
btnRemDressItem = QtBind.createButton(gui,'btnRemDressItem_clicked',"     Remove     ",_x+36+152+3,_y)
btnRemAccesoryItem = QtBind.createButton(gui,'btnRemAccesoryItem_clicked',"     Remove     ",_x+36+152+3+152+3,_y)
btnRemFlagItem = QtBind.createButton(gui,'btnRemFlagItem_clicked',"     Remove     ",_x+36+152+3+152+3+152+3,_y)

_x-=90
btnBuildModel = QtBind.createButton(gui,'btnBuildModel_clicked',"     Build     ",_x,_y-25)
btnClearModels = QtBind.createButton(gui,'btnClearModels_clicked',"     Clear All     ",_x,_y)
# ______________________________ Classes & Methods ______________________________ #

class SRCoord:
	def __init__(self,PosX,PosY,Z,Region):
		# fix to positive region
		if Region < 0:
			Region = 65535+Region+1

		self.region = Region
		if self.inDungeon():
			self.xSector = Region & 0xFF
			self.ySector = Region >> 8

			# phBot dungeon synchronization
			self.x = 10 * ( PosX - (self.xSector - 128) * 192 )
			self.y = 10 * ( PosY - (self.ySector - 128) * 192 )
			
			self.posX = 128 * 192 + self.x / 10
			self.posY = 128 * 192 + self.y / 10
			
			self.xSector = int(((128.0 * 192.0 + self.posX) / 192.0) - 128)
			self.ySector = int(((128.0 * 192.0 + self.posY) / 192.0) - 128)
		else:
			self.posX = PosX
			self.posY = PosY

			self.x = int(abs(PosX) % 192.0 * 10.0)
			if PosX < 0:
				self.x = 1920 - self.x
			self.y = int(abs(PosY) % 192.0 * 10.0)
			if PosY < 0:
				self.y = 1920 - self.y

			self.xSector = int(round((PosX - self.x / 10.0) / 192.0 + 135))
			self.ySector = int(round((PosY - self.y / 10.0) / 192.0 + 92))

		self.z = Z

	def inDungeon(self):
		return self.region > 32767

# Button clicked
def btnSearchItem_clicked():
	# vSRO only
	locale = get_locale()
	if locale != 22:
		return
	# Check is not empty
	itemName = QtBind.text(gui,tbxSearchItem)
	if not itemName:
		return
	# Quick check
	if not isJoined():
		return

	# Create all process on background
	global threadSearching
	if threadSearching:
		return
	# Clear list
	QtBind.clear(gui,lvwItems)
	global lvwItemsData
	lvwItemsData = []

	threadSearching = Thread(target=SearchItem,args=['%'+itemName+'%'])
	threadSearching.run()

# Search an item from silkroad/bot database
def SearchItem(itemName):
	# Creates a connection to database from vsro server
	conn = GetDatabaseConnection(character_data['server'])
	if conn:
		# set cursor
		c = conn.cursor()
		# find items with same name
		c.execute('SELECT id,servername,name,tid3 FROM items WHERE tid1=1 AND tid2=13 AND name LIKE ?',(itemName,))
		global lvwItemsData
		lvwItemsData = c.fetchall()
		# Fill listview
		QtBind.append(gui,lvwItems,'ID | ServerName | Name') # Header
		for item in lvwItemsData:
			QtBind.append(gui,lvwItems,str(item[0])+' | '+item[1]+' | '+item[2])
		# query done
		conn.close()

	# Enable searching
	global threadSearching
	threadSearching = None

# Create a connection to database
def GetDatabaseConnection(server):
	# Load the server info
	data = {}
	with open(bot_path+"/vSRO.json","r") as f:
		data = json.load(f)
	# Match data with the current server
	for k in data:
		servers = data[k]['servers']
		# Check if servers is in list
		if server in servers:
			# Scan data folder
			for path in os.scandir(bot_path+"/Data"):
				# Check databases only
				if path.is_file() and path.name.endswith(".db3"):
					# Connect to check if the data matches
					conn = sqlite3.connect(bot_path+"/Data/"+path.name)
					c = conn.cursor()
					c.execute('SELECT * FROM data WHERE k="path" AND v=?',(data[k]['path'],))
					if c.fetchone():
						# match found
						return conn
					else:
						conn.close()
	return None

# Add the avatar item to the specified list
def btnAddItem_clicked():
	selectedIndex = QtBind.currentIndex(gui,lvwItems)
	# skip header
	if selectedIndex >= 1:
		item = lvwItemsData[selectedIndex-1]

		# Check it's the same genre
		isMale = IsMale(character_data['model'])
		if '_M_' in item[1] or '_W_' in item[1]:
			if (isMale and not '_M_' in item[1]) or (not isMale and not '_W_' in item[1]):
				log('Plugin: Selected item is not matching your character genre!')
				return
		else:
			# Special case - some servers using _F and _M instead
			if (item[1].endswith('_F') and isMale) or (item[1].endswith('_M') and not isMale):
				log('Plugin: Selected item is not matching your character genre!')
				return

		# Select the list
		view = None
		glist = None
		t = item[3]
		if t == 1:
			view = lvwHatItems
			glist = 'lvwHatItemsData'
		elif t == 2:
			view = lvwDressItems
			glist = 'lvwDressItemsData'
		elif t == 3:
			view = lvwAccesoryItems
			glist = 'lvwAccesoryItemsData'
		elif t == 4:
			view = lvwFlagItems
			glist = 'lvwFlagItemsData'

		glist = globals()[glist]
		# Add if doesn't exist
		if not item[0] in glist:
			glist.append(item[0])
			QtBind.append(gui,view,item[2])

# Remove Hat from list
def btnRemHatItem_clicked():
	btnRemoveItem(lvwHatItems,'lvwHatItemsData')

# Remove Dress from list
def btnRemDressItem_clicked():
	btnRemoveItem(lvwDressItems,'lvwDressItemsData')

# Remove Accesory from list
def btnRemAccesoryItem_clicked():
	btnRemoveItem(lvwAccesoryItems,'lvwAccesoryItemsData')

# Remove Flag from list
def btnRemFlagItem_clicked():
	btnRemoveItem(lvwFlagItems,'lvwFlagItemsData')

# Remove avatar item from list
def btnRemoveItem(listview,glistview):
	index = QtBind.currentIndex(gui,listview)
	if index >= 0:
		# Remove it
		glist = globals()[glistview]
		del glist[index]
		# From UI
		QtBind.removeAt(gui,listview,index)

# Creates an avatar model to visualize avatar without buying it
def btnBuildModel_clicked():
	# Quick check
	if not isJoined():
		return

	# Check what has been selected
	index = QtBind.currentIndex(gui,lvwHatItems)
	hat_id = lvwHatItemsData[index] if index >= 0 else 0
	index = QtBind.currentIndex(gui,lvwDressItems)
	dress_id = lvwDressItemsData[index] if index >= 0 else 0
	index = QtBind.currentIndex(gui,lvwAccesoryItems)
	accesory_id = lvwAccesoryItemsData[index] if index >= 0 else 0
	index = QtBind.currentIndex(gui,lvwFlagItems)
	flag_id = lvwFlagItemsData[index] if index >= 0 else 0

	# Create new avatar model
	Inject_Spawn_AvatarModel(hat_id,dress_id,accesory_id,flag_id)

# Clear all avatar models created with this plugin
def btnClearModels_clicked():
	global avatarTestingUID
	delay = 0.01
	if avatarTestingUID:
		for i in range(avatarTestingUID_MIN,avatarTestingUID+1):
			# delete one for one smoothly
			Timer(delay,Inject_Despawn,[i]).start()
			delay+=1
	avatarTestingUID = 0

# Check if character is ingame
def isJoined():
	global character_data
	character_data = get_character_data()
	if not (character_data and "name" in character_data and character_data["name"]):
		character_data = None
	return character_data

# Check if current character is male
def IsMale(model):
	return (model >= 1907 and model <= 1919) or (model >= 14875 and model <= 14887)

def IsChinese(model):
	return model < 14875

# Inject into the client an avatar to visualize the character model
def Inject_Spawn_AvatarModel(hat_id=0,dress_id=0,accesory_id=0,flag_id=0):
	model = character_data['model']

	# All will be done based on current character
	isMale = IsMale(model)
	isChinese = IsChinese(model)
	armor = get_item_string('ITEM_'+('CH' if isChinese else 'EU')+'_'+('M' if isMale else 'W')+'_LIGHT_01_BA_A_DEF')['model']
	legs = get_item_string('ITEM_'+('CH' if isChinese else 'EU')+'_'+('M' if isMale else 'W')+'_LIGHT_01_LA_A_DEF')['model']
	foots = get_item_string('ITEM_'+('CH' if isChinese else 'EU')+'_'+('M' if isMale else 'W')+'_LIGHT_01_FA_A_DEF')['model']
	pos = get_position()
	coord = SRCoord(pos['x'],pos['y'],500,pos['region'])
	avatar = [dress_id,hat_id,accesory_id,flag_id]
	avatarCount = 0
	for a in avatar:
		if a:
			avatarCount += 1
	global avatarTestingUID
	avatarTestingUID = ( (avatarTestingUID+1) if avatarTestingUID else avatarTestingUID_MIN )

	# Create packet
	p = struct.pack('<I',model)
	p += struct.pack('B',0) # scale
	p += struct.pack('B',0) # zerk lv.
	p += struct.pack('B',0) # PVP cape
	p += struct.pack('B',0) # Exp type

	p += struct.pack('B',45) # Inv. Size
	p += struct.pack('B',3) # Inv. Count
	p += struct.pack('<I',armor)
	p += struct.pack('B',0) # plus
	p += struct.pack('<I',legs)
	p += struct.pack('B',0) # plus
	p += struct.pack('<I',foots)
	p += struct.pack('B',0) # plus

	p += struct.pack('B',5) # Avatar Inv. Size
	p += struct.pack('B',avatarCount) # Avatar Inv. Count
	for a in avatar:
		if a:
			p += struct.pack('<I',a)
			p += struct.pack('B',0) # plus

	p += struct.pack('B',0) # has mask

	p += struct.pack('<I',avatarTestingUID) # uid
	p += struct.pack('<H',coord.region)
	p += struct.pack('<f',coord.x)
	p += struct.pack('<f',coord.z)
	p += struct.pack('<f',coord.y)
	p += struct.pack('<H',0) # angle

	p += struct.pack('B',0) # has movement
	p += struct.pack('B',1) # running mode
	p += struct.pack('B',0)
	p += struct.pack('<H',0) # angle

	p += struct.pack('B',1) # life state
	p += struct.pack('B',0)
	p += struct.pack('B',0) # stand up
	p += struct.pack('B',0) # bad status flags

	# Generic Speed
	p += b'\xCD\xCC\x0C\x42\x00\x00\xDC\x42\x00\x00\xC8\x42'

	p += struct.pack('B',0) # buff count
	charName = "[Plugin] AvatarTest #"+str(avatarTestingUID-avatarTestingUID_MIN+1)
	p += struct.pack('H', len(charName))
	p += charName.encode('ascii')

	# Generic job and other stuffs
	p += b'\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xFF\x04'

	# Inject packet to client
	inject_silkroad(0x3015,p,False)

# Inject despawn to the client
def Inject_Despawn(uid):
	inject_silkroad(0x3016,struct.pack('<I',uid),False)

# ______________________________ Events ______________________________ #

# Called when the character enters the game world
def joined_game():
	# Clear all lists to avoid issues
	global lvwHatItemsData, lvwDressItemsData, lvwAccesoryItemsData, lvwFlagItemsData
	QtBind.clear(gui,lvwHatItems)
	lvwHatItemsData = []
	QtBind.clear(gui,lvwDressItems)
	lvwDressItemsData = []
	QtBind.clear(gui,lvwAccesoryItems)
	lvwAccesoryItemsData = []
	QtBind.clear(gui,lvwFlagItems)
	lvwFlagItemsData = []

# Called when the character teleports and right after joined_game()
def teleported():
	global avatarTestingUID
	avatarTestingUID = 0

# Plugin loading ...
log('Plugin: '+pName+' v'+pVersion+' successfully loaded')