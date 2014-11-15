# -*- coding: utf-8-*-
import re
import os
import subprocess
import sys

WORDS = ["PROFILE"]

def handle(text, mic, profile):
	mic.say('May I know who you are ? Write your name please.')
	input = raw_input("Your name : ")
	
	if input=='':
		#Use 'JASPER_CONFIG' environment variable
		os.putenv('JASPER_CONFIG', '/home/malcolm/.jasper')
	else:
		os.putenv('JASPER_CONFIG', '/home/malcolm/.jasper-'+input)
	
	mic.say('Hello '+input+" . You're the new user now" )
	argument = list()
	argument.append(sys.argv[0])
	for arg in sys.argv[1:]:
		argument.append(arg)

	try:
		os.execv("jasper.py",argument) #new environment variable
	except :
		raise

def isValid(text):
    """
        Returns True if input is related to the alarm.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\bprofile\b', text, re.IGNORECASE))