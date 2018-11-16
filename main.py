import sys
import named_entity_tagger as ner

from subprocess import Popen, CREATE_NEW_CONSOLE
from sys import executable

def get_input():
	line = ''

	#Start the Stanford CoreNLP server
	proc1 = Popen([executable, 'core_nlp.py'], cwd='c:\stanford-corenlp-full-2018-02-27', creationflags=CREATE_NEW_CONSOLE)

	try:
		while (line != 'end'):
			line = input('\r\n' + 'Enter a sentence: ')
			if line == 'end':
				print ('Ending Program ...')
				sys.exit()
			else:
				print ('')
				print ('Stanford Named Entities: ')
				formatted_string = ', '.join('{}: {}'.format(*el[::-1]) for el in ner.get_stanford_named_entities(line))
				print (formatted_string)
				print ('')
				print ('NLTK Named Entities: ')
				formatted_string = ', '.join('{}: {}'.format(*el[::-1]) for el in ner.get_nltk_named_entities(line))
				print (formatted_string)
				print ('')
				print ('Spacy Named Entities: ')
				formatted_string = ', '.join('{}: {}'.format(*el[::-1]) for el in ner.get_spacy_named_entities(line))
				print (formatted_string)
				print ('')
				print ('Consolidated Named Entities:')
				formatted_string = ', '.join('{}: {}'.format(*el[::-1]) for el in ner.get_named_entities(line))
				print (formatted_string)

	except KeyboardInterrupt:
		sys.exit()

def main():
	"""
	This is the main entry point for the program
	"""    

	get_input()

if __name__ == "__main__":
	main()