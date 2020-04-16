from phBot import *
import phBotChat
import struct
import time

pName = 'xMatchLocker'
pVersion = '1.1.0'
pUrl = 'https://raw.githubusercontent.com/JellyBitz/phBot-xPlugins/master/xMatchLocker.py'

# User settings
MATCH_PARTY_MASTER = "" # Set party match owner
MATCH_ACADEMY_MASTER = "" # Set academy match owner
QUESTION_PASSWORD = "" # Set password
QUESTION_MESSAGE = "Hi, can you tell me the magic words? Quickly please!"

# ______________________________ Initializing ______________________________ #

# Globals
questionPartyTime = None
questionPartyCharName = ""
questionPartyRID = 0
questionPartyJID = 0
questionAcademyTime = None
questionAcademyCharName = ""
questionAcademyRID = 0
questionAcademyJID = 0

# ______________________________ Methods ______________________________ #

# Inject Packet
def Inject_PartyMatchJoinResponse(requestID,joinID,response):
	p = struct.pack('I', requestID)
	p += struct.pack('I', joinID)
	p += struct.pack('B',1 if response else 0)
	inject_joymax(0x306E,p,False)

# Inject Packet
def Inject_AcademyMatchJoinResponse(requestID,joinID,response):
	p = struct.pack('I', requestID)
	p += struct.pack('I', joinID)
	p += struct.pack('B',1 if response else 0)
	inject_joymax(0x347F,p,False)

# ______________________________ Events ______________________________ #

# All packets received from game server will be passed to this function
# Returning True will keep the packet and False will not forward it to the game client
def handle_joymax(opcode,data):
	# SERVER_PARTY_MATCH_JOIN_REQUEST
	if opcode == 0x706D and QUESTION_PASSWORD:
		try:
			# Save all data for this request
			global questionPartyTime,questionPartyRID,questionPartyJID,questionPartyCharName

			questionPartyTime = time.time()

			index=0
			questionPartyRID = struct.unpack_from('<I',data,index)[0]
			index+=4
			questionPartyJID = struct.unpack_from('<I',data,index)[0]
			index+=22

			charLength = struct.unpack_from('<H',data,index)[0]
			index+=2
			questionPartyCharName = struct.unpack_from('<' + str(charLength) + 's',data,index)[0].decode('cp1252')

			# Send message asking about the password
			phBotChat.Private(questionPartyCharName,QUESTION_MESSAGE)

		except:
			log("Plugin: Oops! Parsing error.. Password doesn't work at this server!")
			log("If you want support, send me all this via private message:")
			log("Data [" + ("None" if not data else ' '.join('{:02X}'.format(x) for x in data))+"] Locale ["+str(get_locale())+"]")
	# SERVER_ACADEMY_MATCH_JOIN_REQUEST
	elif opcode == 0x747E and QUESTION_PASSWORD:
		try:
			# Save all data for this request
			global questionAcademyTime,questionAcademyRID,questionAcademyJID,questionAcademyCharName
			
			questionAcademyTime = time.time()

			index=0
			questionAcademyRID = struct.unpack_from('<I',data,index)[0]
			index+=4
			questionAcademyJID = struct.unpack_from('<I',data,index)[0]
			index+=18

			charLength = struct.unpack_from('<H',data,index)[0]
			index+=2
			questionAcademyCharName = struct.unpack_from('<' + str(charLength) + 's',data,index)[0].decode('cp1252')

			# Send message asking about the password
			phBotChat.Private(questionAcademyCharName,QUESTION_MESSAGE)

		except:
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

	if message == QUESTION_MESSAGE:
		# Create answer but to Master only
		if MATCH_PARTY_MASTER == charName or MATCH_ACADEMY_MASTER == charName:
			phBotChat.Private(charName,QUESTION_PASSWORD)
		else:
			phBotChat.Private(charName,"I'm sorry, you're not my master.. ;)")
		return

	# Check answers

	if charName == questionPartyCharName:
		# Check party match request cancel delay 
		now = time.time()
		if now - questionPartyTime < 5:
			# Check a correct answer
			if message == QUESTION_PASSWORD:
				log("Plugin: "+charName+" joined to party by password")
				Inject_PartyMatchJoinResponse(questionPartyRID,questionPartyJID,True)
			else:
				log("Plugin: "+charName+" canceled party request by wrong password")
				Inject_PartyMatchJoinResponse(questionPartyRID,questionPartyJID,False)
			return

	if charName == questionAcademyCharName:
		# Check academy match request cancel delay 
		now = time.time()
		if now - questionAcademyTime < 5:
			# Check a correct answer
			if message == QUESTION_PASSWORD:
				log("Plugin: "+charName+" joined to academy by password")
				Inject_AcademyMatchJoinResponse(questionAcademyRID,questionAcademyJID,True)
			else:
				log("Plugin: "+charName+" canceled academy request by wrong password")
				Inject_AcademyMatchJoinResponse(questionAcademyRID,questionAcademyJID,False)
			return

# Plugin loaded
log('Plugin: '+pName+' v'+pVersion+' successfully loaded')