from phBot import *
from threading import Timer
import urllib.request
import QtBind
from datetime import datetime
import struct
import json
import os

pName = 'xTranslator'
pVersion = '1.0.0'
pUrl = 'https://raw.githubusercontent.com/JellyBitz/phBot-xPlugins/master/xTranslator.py'

# ______________________________ Initializing ______________________________ #

URL_HOST = "https://phbot-xtranslator.jellybitz.repl.co/api/translate" # API server
URL_REQUEST_TIMEOUT = 10 # sec
SUPPORTED_LANGUAGES = {'Afrikaans':'af','Albanian':'sq','Amharic':'am','Arabic':'ar','Armenian':'hy','Azerbaijani':'az','Basque':'eu','Belarusian':'be','Bengali':'bn','Bosnian':'bs','Bulgarian':'bg','Catalan':'ca','Cebuano':'ceb','Chinese (Simplified)':'zh-CN','Chinese (Traditional)':'zh-TW','Corsican':'co','Croatian':'hr','Czech':'cs','Danish':'da','Dutch':'nl','English':'en','Esperanto':'eo','Estonian':'et','Finnish':'fi','French':'fr','Frisian':'fy','Galician':'gl','Georgian':'ka','German':'de','Greek':'el','Gujarati':'gu','Haitian Creole':'ht','Hausa':'ha','Hawaiian':'haw','Hebrew':'he','Hindi':'hi','Hmong':'hmn','Hungarian':'hu','Icelandic':'is','Igbo':'ig','Indonesian':'id','Irish':'ga','Italian':'it','Japanese':'ja','Javanese':'jv','Kannada':'kn','Kazakh':'kk','Khmer':'km','Kinyarwanda':'rw','Korean':'ko','Kurdish':'ku','Kyrgyz':'ky','Lao':'lo','Latin':'la','Latvian':'lv','Lithuanian':'lt','Luxembourgish':'lb','Macedonian':'mk','Malagasy':'mg','Malay':'ms','Malayalam':'ml','Maltese':'mt','Maori':'mi','Marathi':'mr','Mongolian':'mn','Myanmar (Burmese)':'my','Nepali':'ne','Norwegian':'no','Nyanja (Chichewa)':'ny','Odia (Oriya)':'or','Pashto':'ps','Persian':'fa','Polish':'pl','Portuguese (Portugal, Brazil)':'pt','Punjabi':'pa','Romanian':'ro','Russian':'ru','Samoan':'sm','Scots Gaelic':'gd','Serbian':'sr','Sesotho':'st','Shona':'sn','Sindhi':'sd','Sinhala (Sinhalese)':'si','Slovak':'sk','Slovenian':'sl','Somali':'so','Spanish':'es','Sundanese':'su','Swahili':'sw','Swedish':'sv','Tagalog (Filipino)':'tl','Tajik':'tg','Tamil':'ta','Tatar':'tt','Telugu':'te','Thai':'th','Turkish':'tr','Turkmen':'tk','Ukrainian':'uk','Urdu':'ur','Uyghur':'ug','Uzbek':'uz','Vietnamese':'vi','Welsh':'cy','Xhosa':'xh','Yiddish':'yi','Yoruba':'yo','Zulu':'zu'}

# Globals
character_data = None
locale = None

# Create UI
gui = QtBind.init(__name__,pName)
cbxTranslateIncomingChat = QtBind.createCheckBox(gui,'','Incoming chat messages to',10,8)
cmbxTranslateIncomingLang = QtBind.createCombobox(gui,165,8,130,19)
cbxTranslateOutgoingChat = QtBind.createCheckBox(gui,'','Outgoing chat messages to',10,28)
cmbxTranslateOutgoingLang = QtBind.createCombobox(gui,167,28,128,19)
# Fill with supported langs
for key in SUPPORTED_LANGUAGES:
	QtBind.append(gui,cmbxTranslateIncomingLang,key)
	QtBind.append(gui,cmbxTranslateOutgoingLang,key)

lstTranslatedMessages = QtBind.createList(gui,10,54,710,226)

btnSaveConfig = QtBind.createButton(gui,'save_configs','     Save Changes     ',615,4)
btnClearChat = QtBind.createButton(gui,'btnClearChat_clicked','     Clear chat     ',635,30)

# ______________________________ Methods ______________________________ #

# Return folder path
def get_path():
	return get_config_dir()+pName+"\\"

# Return character configs path (JSON)
def get_config():
	return get_path()+character_data['server'] + "_" + character_data['name'] + ".json"

# Check if character is ingame
def is_joined():
	global character_data
	character_data = get_character_data()
	if not (character_data and "name" in character_data and character_data["name"]):
		character_data = None
	return character_data

# Load default configs
def load_default_config():
	# Default UI and vars
	QtBind.setChecked(gui,cbxTranslateIncomingChat,False)
	QtBind.setChecked(gui,cbxTranslateOutgoingChat,False)

# Save all config
def save_configs():
	# Save if data has been loaded
	if is_joined():
		# Save all data
		data = {}
		data["Incoming Messages"] = QtBind.isChecked(gui,cbxTranslateIncomingChat)
		data["Outgoing Messages"] = QtBind.isChecked(gui,cbxTranslateOutgoingChat)

		data["Incoming Language"] = QtBind.text(gui,cmbxTranslateIncomingLang)
		data["Outgoing Language"] = QtBind.text(gui,cmbxTranslateOutgoingLang)

		# Overrides
		with open(get_config(),"w") as f:
			f.write(json.dumps(data, indent=4, sort_keys=True))
		log("Plugin: "+pName+" configs has been saved")

# Loads all config previously saved
def load_configs():
	load_default_config()
	if is_joined():

		# save locale once
		global locale
		locale = get_locale()

		# Check config exists to load
		if os.path.exists(get_config()):
			data = {}
			with open(get_config(),"r") as f:
				data = json.load(f)
			# Load all data
			if 'Incoming Messages' in data and data['Incoming Messages']:
				QtBind.setChecked(gui,cbxTranslateIncomingChat,True)
			if 'Outgoing Messages' in data and data['Outgoing Messages']:
				QtBind.setChecked(gui,cbxTranslateOutgoingChat,True)

			if "Incoming Language" in data:
				QtBind.setText(gui,cmbxTranslateIncomingLang,data["Incoming Language"])
			if "Outgoing Language" in data:
				QtBind.setText(gui,cmbxTranslateOutgoingLang,data["Outgoing Language"])

# Returns the language ISO369-1 code or an empty string
def get_lang(languageName):
	if languageName in SUPPORTED_LANGUAGES:
		return SUPPORTED_LANGUAGES[languageName]
	return ''

# Translate text to the destination, if the source is not provided it will be auto detected
def translate_text(text,dest,src=''):
	# Check text
	if not text:
		return ''
	# Try to use the API
	try:
		# Create json to be send
		data = {"text":text,"dest":dest}
		if src:
			data['src'] = src
		# Prepare data to send through POST method
		data = json.dumps(data).encode()
		# Create request
		req = urllib.request.Request(URL_HOST,data=data,headers={'content-type':'application/json'})
		with urllib.request.urlopen(req,timeout=URL_REQUEST_TIMEOUT) as f:
			try:
				resp = json.loads(f.read().decode())
				if resp:
					if resp['success']:
						return resp['result']
					else:
						log("Plugin: Translation failed ["+resp['message']+"]")
			except Exception as ex2:
				log("Plugin: Error reading response from server ["+str(ex2)+"]")
	except Exception as ex:
		log("Plugin: Error loading url ["+str(ex)+"] to translate message")
	return ''

# Get the chat type as string
def get_chat_type(t):
	if t == 1:
		return '(All)'
	elif t == 2:
		return '(Private)'
	elif t == 3:
		return '(GM)'
	elif t == 4:
		return '(Party)'
	elif t == 5:
		return '(Guild)'
	elif t == 6:
		return '(Global)'
	elif t == 7:
		return '(Notice)'
	elif t == 9:
		return '(Stall)'
	elif t == 11:
		return '(Union)'
	elif t == 16:
		return '(Academy)'
	return '(Unknown)'

# Called to clear chat list
def btnClearChat_clicked():
	QtBind.clear(gui,lstTranslatedMessages)
# ______________________________ Events ______________________________ #

# All packets received from game server will be passed to this function
# Returning True will keep the packet and False will not forward it to the game client
def handle_joymax(opcode,data):
	# SERVER_CHAT_UPDATE
	if opcode == 0x3026:
		# Check settings
		if not QtBind.isChecked(gui,cbxTranslateIncomingChat):
			return True
		# Starts parsing
		nickname = ''
		chatType = data[0]
		index=1 # packet index
		# uid?
		if chatType in [1,3,13]:
			index+=4
		# nickname? 
		elif chatType in [2,4,5,6,9,11,16]:
			nickLenght = struct.unpack_from('<H', data,index)[0]
			index+=2 # nickLenght
			nickname = struct.unpack_from('<' + str(nickLenght) + 's', data, 8)[0].decode('cp1252')
			index+=nickLenght
		else:
			# Not supported
			return True
		# message
		p = data[:index]
		msgLength = struct.unpack_from('<H',data,index)[0]
		# Check iSRO & TRSRO
		encoding = 'cp1252'
		if locale == 18 or locale == 56:
			msgLength = msgLength*2
			encoding = 'utf-16'
		index+=2 # msgLength
		msg = struct.unpack_from('<' + str(msgLength) + 's',data,index)[0].decode(encoding)
		# Wait for translation without freezing the bot
		def translate_thread():
			lang = get_lang(QtBind.text(gui,cmbxTranslateIncomingLang))
			newMsg = translate_text(msg,lang)
			# Encoding message
			newPacket = p + struct.pack('<H',len(newMsg))
			newPacket += newMsg.encode(encoding) if encoding == 'cp1252' else newMsg.encode(encoding)[2:]
			inject_silkroad(opcode,newPacket,False)
			# Log translation
			text = '< ['+datetime.now().strftime('%H:%M:%S')+']'+ ( ' '+nickname if nickname else '')+' '+get_chat_type(chatType)+':'+newMsg
			QtBind.append(gui,lstTranslatedMessages,text)
		# Run it as thread
		Timer(0.001,translate_thread).start()
		# Ignore it
		return False
	return True

# All packets received from game client will be passed to this function
# Returning True will keep the packet and False will not forward it to the game server
def handle_silkroad(opcode,data):
	# CLIENT_CHAT_REQUEST
	if opcode == 0x7025:
		# Check settings
		if not QtBind.isChecked(gui,cbxTranslateOutgoingChat):
			return True
		# Starts parsing
		chatType = data[0]
		index=1 # packet index
		index+=1 # chat index
		# Check iSRO & TRSRO
		if locale == 18 or locale == 56:
			index+=2
		# private message?
		if chatType == 2:
			index+=2+struct.unpack_from('<H',data,index)[0]
		# message
		p = data[:index]
		msgLength = struct.unpack_from('<H',data,index)[0]
		# Check iSRO & TRSRO
		encoding = 'cp1252'
		if locale == 18 or locale == 56:
			msgLength = msgLength*2
			encoding = 'utf-16'
		index+=2# msgLength
		msg = struct.unpack_from('<' + str(msgLength) + 's',data,index)[0].decode(encoding)
		# Wait for translation without freezing the bot
		def translate_thread():
			lang = get_lang(QtBind.text(gui,cmbxTranslateOutgoingLang))
			newMsg = translate_text(msg,lang)
			# Encoding message
			newPacket = p + struct.pack('<H',len(newMsg))
			newPacket += newMsg.encode(encoding) if encoding == 'cp1252' else newMsg.encode(encoding)[2:]
			inject_joymax(opcode,newPacket,False)
			# Log translation
			text = '> ['+datetime.now().strftime('%H:%M:%S')+'] '+get_chat_type(chatType)+':'+newMsg
			QtBind.append(gui,lstTranslatedMessages,text)
		# Run it as thread
		Timer(0.001,translate_thread).start()
		# Ignore it
		return False
	return True

# Plugin loaded
log("Plugin: "+pName+" v"+pVersion+" successfully loaded")

# Check configs folder
if os.path.exists(get_path()):
	# Add RELOAD plugin support
	load_configs()
else:
	# Creating configs folder
	os.makedirs(get_path())
	log('Plugin: '+pName+' folder has been created')