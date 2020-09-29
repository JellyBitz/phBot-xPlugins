from phBot import *
from threading import Timer
import struct

pName = 'xCarnivalBalloon'
pVersion = '1.0.0'
pUrl = 'https://raw.githubusercontent.com/JellyBitz/phBot-xPlugins/master/xCarnivalBalloon.py'

# ______________________________ Initializing ______________________________ #

INFLATE_BALLOON_LEVEL_STOP = 6
INFLATE_BALLOON_LEVELUP_DELAY = 4.0 # seconds

isInflating = False
inflatingLevel = 0

# ______________________________ Methods ______________________________ #

# Search an item by name or servername through lambda expression and return his information.
def GetItemByExpression(_lambda):
	items = get_inventory()['items']
	for slot, item in enumerate(items):
		if item:
			# Search by lambda
			if _lambda(item['name'],item['servername']):
				# Save slot location
				item['slot'] = slot
				return item
	return None

# Inflates a balloon
def InflateNewBalloon():
	item = GetItemByExpression(lambda n,s: s.startswith('ITEM_ETC_E101216_BALLOON_'))
	# Check if balloon has been found
	if item:
		# Tracking balloon level
		global inflatingLevel
		inflatingLevel = 1
		# Build packet and use it
		p = struct.pack('B',item['slot'])
		p += b'\x30\x0C\x09\x00'
		log('Plugin: Using "'+item['name']+'"...')
		inject_joymax(0x704C,p,True)
		# Start leveling it after passing delay
		Timer(INFLATE_BALLOON_LEVELUP_DELAY,LevelUpBalloon).start()
	else:
		global isInflating
		isInflating = False
		# Start bot and get back to town
		log('Plugin: Balloons not found, using return scroll...')
		use_return_scroll()
		# All done, just Start it
		start_bot()

# Inflates a balloon to the next level
def LevelUpBalloon():
	# Check if can claim it
	if inflatingLevel >= (INFLATE_BALLOON_LEVEL_STOP-1):
		# Claim balloon
		log('Plugin: Getting balloon reward (Lv.'+str(balloonLevel)+')')
		inject_joymax(0x7574,b'\x02',False)
		balloonLevel = 0
		# Continue
		Timer(INFLATE_BALLOON_LEVELUP_DELAY,LevelUpBalloon).start()
	# Check if ballon is alive
	elif inflatingLevel:
		# Try level up
		log('Plugin: Inflating balloon...')
		inject_joymax(0x7574,b'\x01',False)
		# Try to level up it again
		Timer(INFLATE_BALLOON_LEVELUP_DELAY,LevelUpBalloon).start()
	# Try to inflate another one
	else:
		InflateNewBalloon()

# Made for condition usage only
def InflateBalloons():
	# avoid trigger it multiple times
	if not isInflating:
		inflate_balloons([])
# ______________________________ Events ______________________________ #

# Starts inflating balloons through script command
def inflate_balloons(args):
	item = GetItemByExpression(lambda n,s: s.startswith('ITEM_ETC_E101216_BALLOON_'))
	# Check if balloon has been found
	if item:
		# Stop scripting
		stop_bot()
		# Start inflating process
		global isInflating
		isInflating = True
		log('Plugin: Starting to inflate balloons...')
		# Avoid interpreter lock
		Timer(0.001,InflateNewBalloon).start()
	else:
		log('Plugin: Balloons not found on your inventory')
	return 0

# All packets received from game server will be passed to this function
# Returning True will keep the packet and False will not forward it to the game client
def handle_joymax(opcode,data):
	# SERVER_BALLOON_UP_RESPONSE
	if opcode == 0xB574 and isInflating:
		# inflated
		if data[0] == 1:
			global inflatingLevel
			# update new level
			if data[1] == 1: # up
				inflatingLevel += 1
			elif data[1] == 2: # fail
				inflatingLevel = 0
	return True

# Plugin loaded
log('Plugin: '+pName+' v'+pVersion+' successfully loaded')