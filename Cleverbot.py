# -*- coding: utf-8-*-
from sys import maxint
import cleverbot
import sys
from client import diagnose

WORDS = []

PRIORITY = -(maxint)

cb1 = cleverbot.Cleverbot()

'''
#TODO :
Make this a hight priority module that goes first, detect if the sentence is an "order" or a "conversation" sentence. If it's the first one, go on doing the order, if the second just send the request to Cleverbot.
'''

def cleverbotRequest(text, mic, profile):
	#TODO maybe a more pythonic way to do this
	flag=0
	for arg in sys.argv[1:]:
		if(arg == '--no-network-check'):
			flag=1
			
	if flag==1 and not diagnose.check_network_connection():
		Unclear.handle(text, mic, profile)
	else:
		answer = cb1.ask(text)
		mic.say(answer)

def handle(text, mic, profile):
	"""
		Talk with the user using Cleverbot if no command were understood

		Arguments:
		text -- user-input, typically transcribed speech
		mic -- used to interact with the user (for both input and output)
		profile -- contains information related to the user (e.g., phone
					number)
	"""
	cleverbotRequest(text, mic, profile)


def isValid(text):
    return True
