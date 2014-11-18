# -*- coding: utf-8-*-
import duckduckgo
import re

WORDS = ["DUCKDUCKGO", "SEARCH", "GOOGLE"]

#Word determine as useless in a search
useless_search_word = ["a", "and", "the"]


def getResults(question, mic):
	result=duckduckgo.query(question)
	flag=True
	switch=False
	count=0
	count_topics=0

	if result.type!='nothing':
		while flag:
			try:
				if(switch==False):	
					mic.say(result.related[count].text)
				else:
					mic.say(result.related[count].topics[count_topics].text)
				mic.say('Were you talking about this ?')
				yesno=mic.activeListen()
				if yesno=='no' and count<len(result.related)-1:
					if switch==False:
						count=count+1
					else:
						if(count_topics==len(result.related[count].topics)-1):
							count_topics=0
							count=count+1
						else:
							count_topics=count_topics+1
				elif yesno=='yes' :
					flag=False
					mic.say('Glad I could help you')
				else:
					flag=False
					mic.say("OK I'll stop")
			#Switch to topics
			except Exception:
				switch=True

	else :
		#get the best results
		mic.say('I had no results. Here is my best shot !')
		mic.say(duckduckgo.get_zci(question))


def handle(text, mic, profile):
	"""
        Search on duckduckgo for information

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
    """
	if re.search('what is',text):
		#print re.split('what is', text)
		#get last element
		question=re.split('what is', text)[-1]
		question=" ".join("" if s in useless_search_word else s for s in question.split())

	else:
		mic.say('What would like me to search ?')
		question=mic.activeListen()
		question=" ".join("" if s in useless_search_word else s for s in question.split())
	
	getResults(question, mic)
	
def isValid(text):
    """
        Returns True if the input is related to the meaning of life.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\bduckduckgo|search|google\b', text, re.IGNORECASE))
