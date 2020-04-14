from phBot import *
import phBotChat
import struct
import time

pName = 'xPartyMatchLocker'
pVersion = '0.0.2'
pUrl = 'https://raw.githubusercontent.com/JellyBitz/phBot-xPlugins/master/xPartyMatchLocker.py'

# User settings
QUESTION_PASSWORD = "" # Set password to lock part match join requests

# Globals
questionMessage = "Hi, can you tell me the password? Please, quickly!"
questionTime = None
questionCharName = ""
questionJID = 0
questionRID = 0

# All packets received from Silkroad will be passed to this function
# Returning True will keep the packet and False will not forward it to the game server
def handle_joymax(opcode,data):
	# SERVER_PARTY_MATCH_JOIN_REQUEST
	if opcode == 0x706D and QUESTION_PASSWORD:
		# Tested on vSRO only
		try:
			# init cursor
			index=0
			requestID = struct.unpack_from('<I',data,index)[0]
			index+=4
			joinID = struct.unpack_from('<I',data,index)[0]
			index+=22

			charLength = struct.unpack_from('<H',data,index)[0]
			index+=2
			charName = struct.unpack_from('<' + str(charLength) + 's',data,index)[0].decode('cp1252')
			#index+=charLength

			# Save all data for this request
			questionTime = time.time()
			questionCharName = charName
			questionJID = joinID
			questionRID = requestID

			# Send message asking about the password
			phBotChat.Private(charName,questionMessage)

		except Exception as e:
			log("Plugin: Oops! Parsing error.. Password doesn't work at this server!")
			log("If you want support, send me all this via private message:")
			log("Data [" + ("None" if not data else ' '.join('{:02X}'.format(x) for x in data))+"] Locale ["+str(get_locale())+"]")
	return True

# All chat messages received are sent to this function
def handle_chat(t,charName,message):
	# Check private messages only
	if t != 2:
		return
	# Analyze only if the password has been set
	if not QUESTION_PASSWORD:
		return

	# Check questions
	if message == questionMessage:
		# Create answer
		phBotChat.Private(charName,QUESTION_PASSWORD)
	# Check answers
	elif charName == questionCharName:
		# Check party match request cancel delay 
		now = time.time()
		if now - questionTime > 5:
			return
		# Check a correct answer
		if message == QUESTION_PASSWORD:
			log("Plugin: "+charName+" joined to party by password")
			Inject_PartyMatchJoinResponse(questionRID,questionJID,True)
		else:
			log("Plugin: "+charName+" canceled by wrong password")
			Inject_PartyMatchJoinResponse(questionRID,questionJID,False)

# Inject Packet
def Inject_PartyMatchJoinResponse(requestID,joinID,response):
	p = struct.pack('I', requestID)
	p += struct.pack('I', joinID)
	p += struct.pack('B',1 if response else 0)
	inject_joymax(0x306E,p,False)

# Plugin load success
log('Plugin: '+pName+' v'+pVersion+' successfully loaded')