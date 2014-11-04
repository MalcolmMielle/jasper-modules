'''
I should make a passive silent Module, see Jasper API
'''

# -*- coding: utf-8-*-
import datetime
import re
import os
from app_utils import getTimezone
from semantic.dates import DateService

WORDS = ["ALARM"]

def handle(text, mic, profile):
	"""
        Set up an alarm clock

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
    """
	mic.say("Setting up alarm")
	#Setting arguments
	#Ask for th hour
	mic.say("Here are the current top headlines. " + all_titles +
                ". Would you like me to send you these articles? " +
                "If so, which?")
	#Listen to the answer
	handleResponse(mic.activeListen())
	hour = 21
	min = 43
	
	"""
		Fork the process. Child is an alarm clock while the parent continue Jasper.
		Problem with multiple alarm being multiple process instead of having only one with multiple time :S
	"""
	
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
	
	
	
def isValid(text):
    """
        Returns True if input is related to the alarm.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\balarm\b', text, re.IGNORECASE))