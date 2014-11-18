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


#Text to number function : 
#From https://github.com/ghewgill/text2num

Small = {
    'zero': 0,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    'ten': 10,
    'eleven': 11,
    'twelve': 12,
    'thirteen': 13,
    'fourteen': 14,
    'fifteen': 15,
    'sixteen': 16,
    'seventeen': 17,
    'eighteen': 18,
    'nineteen': 19,
    'twenty': 20,
    'thirty': 30,
    'forty': 40,
    'fifty': 50,
    'sixty': 60,
    'seventy': 70,
    'eighty': 80,
    'ninety': 90
}

Magnitude = {
    'thousand':     1000,
    'million':      1000000,
    'billion':      1000000000,
    'trillion':     1000000000000,
    'quadrillion':  1000000000000000,
    'quintillion':  1000000000000000000,
    'sextillion':   1000000000000000000000,
    'septillion':   1000000000000000000000000,
    'octillion':    1000000000000000000000000000,
    'nonillion':    1000000000000000000000000000000,
    'decillion':    1000000000000000000000000000000000,
}

class NumberException(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)

def text2num(s):
    a = re.split(r"[\s-]+", s)
    n = 0
    g = 0
    for w in a:
        x = Small.get(w, None)
        if x is not None:
            g += x
        elif w == "hundred":
            g *= 100
        else:
            x = Magnitude.get(w, None)
            if x is not None:
                n += g * x
                g = 0
            else:
                raise NumberException("Unknown number: "+w)
    return n + g


#Alarm clock thread function

def alarmclock(profile, mic,*args):

	print 'set up !'

	while(len(hours)!=0):
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
		lock.release()
	print 'exit, no more alarm to ring'
	

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
	#Ask for the hour
	#Listen to the answer
	hour=mic.activeListen()
	hour=text2num(hour)
	hour=int(hour)
	
	mic.say("And minute ?")
	min=mic.activeListen()
	min=text2num(min)
	min=int(min)
	
	lock.acquire(True)
	hours.append( (hour, min) )
	lock.release()
	
	if(len(hours)==1):
		Thread(target=alarmclock,args=(profile,mic,1)).start()
	
	
def isValid(text):
    """
        Returns True if input is related to the alarm.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\balarm\b', text, re.IGNORECASE))