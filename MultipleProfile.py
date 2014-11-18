# -*- coding: utf-8-*-
import re
import os
import subprocess
import sys
import logging
import shutil
import yaml
import copy

from client import tts, stt, jasperpath, diagnose



WORDS = ["PROFILE", "WHO AM I"]

def getNewProfile(mic, profile):
	
	mic.say('May I know who you are ? Write your name please.')
	input = raw_input("Your name : ")
	
	if input=='':
		profile_file='profile.yml'
	else:
		profile_file='profile-'+input+'.yml'
	
	mic.say('Hello '+input+" . You're the new user now" )
	
	#TODO replace by directly reading the config file and changing the var profile 
	#argument = list()
	#argument.append(sys.argv[0])
	#for arg in sys.argv[1:]:
#		argument.append(arg)
	
	logger = logging.getLogger(__name__)

	# FIXME: For backwards compatibility, move old config file to newly
	#        created config dir
	old_configfile = os.path.join(jasperpath.LIB_PATH, profile_file)
	new_configfile = jasperpath.config(profile_file)
	if os.path.exists(old_configfile):
		if os.path.exists(new_configfile):
			logger.warning("Deprecated profile file found: '%s'. " +
									"Please remove it.", old_configfile)
		else:
			logger.warning("Deprecated profile file found: '%s'. " +
									"Trying to copy it to new location '%s'.",
									old_configfile, new_configfile)
			try:
				shutil.copy2(old_configfile, new_configfile)
			except shutil.Error:
				logger.error("Unable to copy config file. " +
									"Please copy it manually.",
									exc_info=True)
				raise

	# Read config
	logger.debug("Trying to read config file: '%s'", new_configfile)
	try:
		with open(new_configfile, "r") as f:
			#Where the magic is. Clear the dict and then update it
			profile.clear()
			profile.update(yaml.safe_load(f))
	except OSError:
		logger.error("Can't open config file: '%s'", new_configfile)
		raise


	try:
		api_key = profile['keys']['GOOGLE_SPEECH']
	except KeyError:
		api_key = None

	try:
		stt_engine_type = profile['stt_engine']
	except KeyError:
		stt_engine_type = "sphinx"
		logger.warning("stt_engine not specified in profile, " +
								"defaulting to '%s'", stt_engine_type)

	try:
		tts_engine_slug = profile['tts_engine']
	except KeyError:
		tts_engine_slug = tts.get_default_engine_slug()
		logger.warning("tts_engine not specified in profile, defaulting " +
						"to '%s'", tts_engine_slug)
	tts_engine_class = tts.get_engine_by_slug(tts_engine_slug)

	#TODO To test !
	flag=0
	for arg in sys.argv[1:]:
		if(arg == '--local'):
			from client.local_mic import Mic
			flag=1
	if flag==0:
		from client.mic import Mic

	# Initialize Mic
	mic = Mic(tts_engine_class(),
					stt.PocketSphinxSTT(**stt.PocketSphinxSTT.get_config()),
					stt.newSTTEngine(stt_engine_type, api_key=api_key))
					
	
def sayWhoYouAre(mic, profile):
	mic.say('This is who you are to me : ')
	mic.say('Your name is : '+profile['first_name'])
	mic.say('Your family name is : '+profile['last_name'])
	mic.say('You live at : '+profile['location'])
	mic.say('Your gmail account is : '+profile['gmail_address'])
	

def handle(text, mic, profile):
	
	if re.search('profile', text):
		getNewProfile(mic, profile)
	else:
		sayWhoYouAre(mic, profile)	

def isValid(text):
    """
        Returns True if input is related to the alarm.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\bprofile|who am I\b', text, re.IGNORECASE))