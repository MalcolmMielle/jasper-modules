# -*- coding: utf-8-*-
import re
import recipepuppy
import pickle

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
		with open('~/.inventory/inventory.inv', 'r') as filename:
			inventoryarr = pickle.load(filename)
			filename.close()
			list_item=inventoryarr.items()
			#Query a receipe
			mic.say(recipepuppy.get_recipe(list_item))
	except IOError:
		mic.say("No inventory on computer. I can't find your food. Make sure it's at ~/.inventory/inventory.inv")
	

def isValid(text):
    """
        Returns True if the input is related to the meaning of life.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\brecipe\b', text, re.IGNORECASE))