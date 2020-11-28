from phBot import *
import phBotChat
import QtBind
import json
import os
import re

pName = 'xTrivia'
pVersion = '0.1.3'
pUrl = 'https://raw.githubusercontent.com/JellyBitz/phBot-xPlugins/master/xTrivia.py'

# ______________________________ Initializing ______________________________ #

# Globals
character_data = None
trivia_data = []
trivia_last_question = ''

# Graphic user interface
gui = QtBind.init(__name__,pName)

lblDescription = QtBind.createLabel(gui,"xTrivia can automatically save all the questions with the answers if you supply the correct pattern (regex).\nIt is working with Notice chat only and sending the question to General chat by default.",6,10)

lblQuestionPattern = QtBind.createLabel(gui,"Question Pattern :",6,45)
tbxQuestionPattern = QtBind.createLineEdit(gui,"",98,43,350,19)

lblAnswerPattern = QtBind.createLabel(gui,"Answer Pattern :",6,65)
tbxAnswerPattern = QtBind.createLineEdit(gui,"",90,63,358,19)

lblReplyTo = QtBind.createLabel(gui,"Reply To :",480,55)
tbxReplyTo = QtBind.createLineEdit(gui,"",530,53,80,19)

btnSaveConfig = QtBind.createButton(gui,'saveConfigs',"     Save     ",645,4)


lblQuestion = QtBind.createLabel(gui,"Question :",6,105)
tbxQuestion = QtBind.createLineEdit(gui,"",59,103,180,19)
lblAnswer = QtBind.createLabel(gui,"Answer :",59+180+6,105)
tbxAnswer = QtBind.createLineEdit(gui,"",59+180+6+48,103,90,19)
btnAddTrivia = QtBind.createButton(gui,'btnAddTrivia_clicked',"     Add     ",59+180+6+48+90+6,105-4)
btnRemTrivia = QtBind.createButton(gui,'btnRemTrivia_clicked',"     Remove     ",720-75-6,105-4)
lstTriviaData = QtBind.createList(gui,6,125,720-12,18*8-3)

# ______________________________ Methods ______________________________ #

# Return folder path
def getPath():
	return get_config_dir()+pName+"\\"

# Return character configs path (JSON)
def getConfigPath():
	return getPath()+character_data['server'] + "_" + character_data['name'] + ".json"

# Return trivia config path for the server
def getTriviaPath():
	return getPath()+"_"+character_data['server'] + "_Trivia.json"

# Check if character is ingame
def isJoined():
	global character_data
	character_data = get_character_data()
	if not (character_data and "name" in character_data and character_data["name"]):
		character_data = None
	return character_data

# Save all config
def saveConfigs():
	# Save if data has been loaded
	if isJoined():
		# Save all data
		data = {}

		data['QuestionPattern'] = QtBind.text(gui,tbxQuestionPattern)
		data['AnswerPattern'] = QtBind.text(gui,tbxAnswerPattern)
		data['ReplyTo'] = QtBind.text(gui,tbxReplyTo)

		# Overrides
		with open(getConfigPath(),"w") as f:
			f.write(json.dumps(data, indent=4, sort_keys=True))
		log("Plugin: "+pName+" configs has been saved")

# Load default configs
def loadDefaultConfig():
	# Clear data
	QtBind.setText(gui,tbxQuestionPattern,"")
	QtBind.setText(gui,tbxAnswerPattern,"")
	QtBind.setText(gui,tbxReplyTo,"")
	
	QtBind.clear(gui,lstTriviaData)

# Loads all config previously saved
def loadConfigs():
	loadDefaultConfig()
	if isJoined():
		# Check config exists to load
		if os.path.exists(getConfigPath()):
			data = {}
			with open(getConfigPath(),"r") as f:
				data = json.load(f)
			# Load data
			if "QuestionPattern" in data and data["QuestionPattern"]:
				QtBind.setText(gui,tbxQuestionPattern,data["QuestionPattern"])
			if "AnswerPattern" in data and data["AnswerPattern"]:
				QtBind.setText(gui,tbxAnswerPattern,data["AnswerPattern"])
			if "ReplyTo" in data and data["ReplyTo"]:
				QtBind.setText(gui,tbxReplyTo,data["ReplyTo"])
		# Try to load trivia data for first time
		UpdateTriviaData()

# Load the trivia data
def UpdateTriviaData():
	# Clean it
	global trivia_data
	trivia_data = []
	QtBind.clear(gui,lstTriviaData)
	# Check the trivia data
	if os.path.exists(getTriviaPath()):
		# Try to Load trivia file
		with open(getTriviaPath(),"r") as f:
			trivia_data = json.load(f)
		# Load the listview
		for trivia in trivia_data:
			QtBind.append(gui,lstTriviaData,'Q: "'+trivia['q']+'" A: "'+trivia['a']+'"')


# Return True if the question exist into the array
def QuestionExists(_array,_question):
	for _value in _array:
		if _value['q'] == _question:
			return True
	return False

# Add question answer to database
def AddQuestionAnswer(question,answer):
	# Check question existence
	if not QuestionExists(trivia_data,question):
		# Create trivia object
		trivia = {'q':question,'a':answer}
		# Insert ordered into the list
		index = 0
		for data in trivia_data:
			if data['q'] > question:
				break
			index+=1
		trivia_data[index:index] = [trivia]

		trivia_text = 'Q: "'+question+'" A: "'+answer+'"'
		# Overwrite file
		with open(getTriviaPath(),"w") as f:
			f.write(json.dumps(trivia_data, indent=4, sort_keys=True))
		# Update all
		UpdateTriviaData()
		# Success message
		log('Plugin: Trivia ['+trivia_text+'] has been added')

# Add trivia manually
def btnAddTrivia_clicked():
	# avoid empty data
	question = QtBind.text(gui,tbxQuestion)
	if not question:
		return
	answer = QtBind.text(gui,tbxAnswer)
	if not answer:
		return
	# update it at first
	UpdateTriviaData()
	# try to add it
	AddQuestionAnswer(question,answer)
	# reset data
	QtBind.setText(gui,tbxQuestion,'')
	QtBind.setText(gui,tbxAnswer,'')

# Remove trivia manually
def btnRemTrivia_clicked():
	# get index selected
	index = QtBind.currentIndex(gui,lstTriviaData)
	if index >= 0:
		global trivia_data
		# save the data to be deleted
		trivia = trivia_data[index]
		# update it at first
		UpdateTriviaData()
		# search the trivia index to be deleted
		index = -1
		for i in range(len(trivia_data)):
			if trivia_data[i]['q'] == trivia['q']:
				index = i 
				break
		if index != -1:
			del trivia_data[index]
			QtBind.removeAt(gui,lstTriviaData,index)
			# Overwrite the file
			with open(getTriviaPath(),"w") as f:
				f.write(json.dumps(trivia_data, indent=4, sort_keys=True))
		# Success message
		log('Plugin: Trivia ['+trivia['q']+'] has been removed')

# Binary search algorithm. Returns the index or -1 if is the element is not found
def binarySearch(_array, _left, _right, _element): 
	# Check base case
	if _right >= _left:
		mid = _left + (_right - _left) // 2
		if _array[mid]['q'] == _element:
			return mid
		elif _array[mid]['q'] > _element: 
			return binarySearch(_array, _left, mid-1, _element)
		else: 
			return binarySearch(_array, mid+1, _right, _element)
	else:
		return -1

# Returns the answer to the question, otherwise empty is returned
def FindAnswer(Question):
	UpdateTriviaData()
	# Check if is not empty
	if trivia_data:
		# Try to find it asap 
		index = binarySearch(trivia_data,0,len(trivia_data)-1,Question)
		# Check existence of the question
		if index != -1:
			# Return the answer
			return trivia_data[index]['a']
	# Nothing found
	return None

# Send the message to the player or to all chat 
def SendAnswer(Answer):
	playerToReply = QtBind.text(gui,tbxReplyTo)
	if playerToReply:
		phBotChat.Private(playerToReply,Answer)
	else:
		phBotChat.All(Answer)

# Search and reply the trivia question
def ReplyQuestion(Question):
	global trivia_last_question
	# Try to find the answer
	answer = FindAnswer(Question)
	# Check answer
	if answer == None:
		log('Plugin: Trivia answer not found! ['+Question+']')
		# Keep in memory the last question made and not answered
		trivia_last_question = Question
	else:
		# Answering as quickly as possible (:
		SendAnswer(answer)
		log('Plugin: Trivia answer sent ['+answer+']')
		# clean it just in case
		trivia_last_question = ""

# Save the trivia question/answer into the books ;)
def SaveAnswer(Answer):
	# Cannot save it if there is no question previously saved
	if trivia_last_question:
		global trivia_data
		# Update it the gui and data at first
		UpdateTriviaData()
		# Try to add it
		AddQuestionAnswer(trivia_last_question,Answer)

# Check if the message pattern is correct to reply to the question
def CheckQuestionPattern(msg):
	# Check the question pattern
	questionPattern = QtBind.text(gui,tbxQuestionPattern)
	if questionPattern:
		try:
			if re.search(questionPattern,msg):
				ReplyQuestion(msg)
				return True
		except Exception as ex:
			log("Plugin: Error at regex ["+str(ex)+"]")
	return False

# Check if the answer pattern is correct to save the answer
def CheckAnswerPattern(msg):
	# Check the answer pattern
	answerPattern = QtBind.text(gui,tbxAnswerPattern)
	if answerPattern:
		try:
			# The match needs to be grouped, otherwise is not going to work
			match = re.findall(answerPattern,msg)
			if match:
				if type(match[0]) is tuple:
					# Remove empty matches
					match[0] = list(filter(None, match[0]))[1]
				# Save first match
				SaveAnswer(match[0])
				return True
		except Exception as ex:
			log("Plugin: Error at regex ["+str(ex)+"]")
	return False
# ______________________________ Events ______________________________ #

# Called when the character enters the game world
def joined_game():
	loadConfigs()

# All chat messages received are sent to this function
def handle_chat(t,player,msg):
	# Check a notice message
	if t == 7:
		# Just try to check stuffs on this message
		CheckQuestionPattern(msg)
		CheckAnswerPattern(msg)

# Plugin loaded
log('Plugin: '+pName+' v'+pVersion+' successfully loaded')

if os.path.exists(getPath()):
	# Adding RELOAD plugin support
	loadConfigs()
else:
	# Creating configs folder
	os.makedirs(getPath())
	log('Plugin: '+pName+' folder has been created')