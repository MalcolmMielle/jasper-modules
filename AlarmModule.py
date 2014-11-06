'''
Made it a thread.
'''

# -*- coding: utf-8-*-
import datetime
import re
import os
import subprocess
from threading import Thread, Lock
from app_utils import getTimezone
from semantic.dates import DateService

WORDS = ["ALARM"]

hours = []
lock = Lock()

def alarmclock(profile, mic,*args):
	print 'set up !'
	finished=1
	while(finished == 1):
		tz = getTimezone(profile)
		now = datetime.datetime.now(tz=tz)
		lock.acquire(True)
		for i, (h, m) in enumerate (hours):
			hour_now = now.hour
			min_now = now.minute
			#mic.say("it is now %s %s and alarm is %s %s" % (hour_now, min_now, h, m))

			if(hour_now==h and min_now==m):
				print 'ringing !'
				#TODO integrate it with xbmc
				cmd='vlc '+profile['alarm_file']
				print cmd
				subprocess.Popen(cmd, shell=True) 
				#suppress the hour if ringed
				del hours[i]
				finished=0
		lock.release()
	print 'exit'
	

def handle(text, mic, profile):
	"""
        Set up an alarm clock

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
    """
	mic.say("Setting up alarm, what hour do you want it to ring ?")
	#Setting arguments
	#Ask for th hour
	#Listen to the answer
	hour=mic.activeListen()
	hour=int(hour)
	
	mic.say("And minute ?")
	min=mic.activeListen()
	min=int(min)
	
	lock.acquire(True)
	hours.append( (hour, min) )
	lock.release()
	
	if(len(hours)==1):
		Thread(target=alarmclock,args=(profile,mic,1)).start()
	
	"""
		Fork the process. Child is an alarm clock while the parent continue Jasper.
		Problem with multiple alarm being multiple process instead of having only one with multiple time :S
	"""
	thefile = open(os.path.join(os.path.dirname(__file__),'AlarmFile.txt'), 'w')
	try:
		thefile.write("hour : %s min : %s\n" % (hour, min))
	finally:
		thefile.close()
	
	
	'''
	newpid = os.fork()
	if newpid == 0:
		print 'Your alarm clock is the process ',  os.getpid( )
		finished=1
		while(finished == 1):
			tz = getTimezone(profile)
			now = datetime.datetime.now(tz=tz)
			hour_now = now.hour
			min_now = now.minute
			#mic.say("it is now %s %s ad alarm is %s %s" % (hour_now, min_now, hour, min))
			if(hour_now==hour and min==min_now):
				print 'ringing !'
				finished=0
		print 'exit'
		os._exit(0)  
	else:
		pids = (os.getpid(), newpid)
		print "parent: %d, child: %d" % pids
	'''
	
	
def isValid(text):
    """
        Returns True if input is related to the alarm.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\balarm\b', text, re.IGNORECASE))