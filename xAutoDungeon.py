from phBot import *
from threading import Timer

pVersion = 'v0.0.4'

check_mobs_time = 0
isAttacking = False
ignoreGhostCurse = True

# Attack all mobs around using the bot config. Ex: "AttackArea" or "AttackArea,15"
# Will be checking mobs every 15 seconds at this area as default.
def AttackArea(arguments):
	# stop bot and kill mobs through bot or continue script normally
	if getMobCount() > 0:
		# stop scripting
		stop_bot()
		# set automatically the training area
		p = get_position()
		set_training_position(p['region'], p['x'], p['y'])
		# set time
		if len(arguments) == 2:
			check_mobs_time = float(arguments[1])
		#15s as default
		if not check_mobs_time:
			global check_mobs_time
			check_mobs_time = 15.0
		# start to kill mobs on other thread because interpreter lock
		Timer(1.0,AttackMobs).start()
	# otherwise continue normally
	else:
		log("Plugin: Not mobs at this area.")
	return 0

# Attacking mobs using all configs from bot
def AttackMobs():
	if getMobCount() > 0:
		# Start to kill mobs with last training area
		if not isAttacking:
			start_bot()
			global isAttacking
			isAttacking = True
		log("Plugin: Killing ("+str(getMobCount())+") mobs at this area.")
		# Check if there is not mobs to continue the script
		Timer(check_mobs_time,AttackMobs).start()
	else:
		# All mobs killed, stop botting
		stop_bot()
		global isAttacking
		isAttacking = False
		# Setting training area far away. The bot should continue where he was at the script
		set_training_position(0,0,0)
		log("Plugin: All mobs killed. Getting back to the script.")
		Timer(1,start_bot).start()

# Count all mobs around your character (60 or more it's the max. range I think)
def getMobCount():
	count = 0
	monsters = get_monsters()
	if monsters:
		for mob in monsters:
			if ignoreGhostCurse and monsters[mob]["name"].lower() == "ghost curse":
				continue
			count+=1
	return count

log('Plugin: xAutoDungeon '+pVersion+' succesfully loaded.')