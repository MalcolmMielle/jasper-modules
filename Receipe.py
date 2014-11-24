# -*- coding: utf-8-*-
#!/usr/bin/python
import re
import recipepuppy
import pickle
import os

import webbrowser

WORDS = ["RECIPE"]

def handle(text, mic, profile):
	"""
        Search for a receipe on Receipe Puppy
        This must be use with the inventory package https://github.com/MalcolmMielle/inventory forked from https://github.com/wbrenna/inventory
        
        One need to install the receipe Puppy python library from https://github.com/MalcolmMielle/python_recipepuppy

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
    """
	try:
		with open(os.path.expanduser('~/.inventory/inventory.inv'), 'r') as filename:
			inventoryarr = pickle.load(filename)
			filename.close()
			lst=list()
			for upc in inventoryarr.keys():
				for key in inventoryarr[upc][1:]:
					if inventoryarr[upc][0][1] is not None:
						lst.append(inventoryarr[upc][0][1])
			print lst
			#Query a receipe
			flag=0
			res=recipepuppy.get_full_info(ingredient=lst).data
			for key in res:
				mic.say('Would you like to cook '+key)
				mic.say('You would need to have : '+res[key])
			#webbrowser.open(res.link)

	except IOError:
		mic.say("No inventory on computer. I can't find your food. Make sure it's at ~/.inventory/inventory.inv")
	

def isValid(text):
    """
        Returns True if the input is related to the meaning of life.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\brecipe\b', text, re.IGNORECASE))