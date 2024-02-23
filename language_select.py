import importlib

def change_language():
	lan_select = input('Change language from English? Press (Y) for yes. Otherwise it stays English.\n')
	lan = 'en'
	try:
		# Check if the user wants to change the language
		# if not, exit with EN
		if lan_select.upper() != 'Y':
			return lan
		
		print('Warning. Must be online to be able to use the Google translate function.\n')

		all_languages = input('If you want to see the list of available languages, press (A)\n')
	
		# lazy loading:
		googletrans = importlib.import_module('googletrans')
		# Use the googletrans module here
		constants = googletrans.constants
		
		# Print the list of available languages and their codes
		if all_languages.upper() == 'A':
			print(f'The available languages and their codes are:\n{constants.LANGCODES}')

		lan = input('\nPlease enter your desired language (2 letter code, e.g "en" = English, "hu" = Magyar, "de" = Deutsch):\n').strip()	

		while True:
			lan = lan.lower()
			try:
				# Check if the language code is valid or raise exc
				if lan in constants.LANGUAGES:
					break
				else:
					raise ValueError('Not a valid code!\n')
			except ValueError as e:
				# Handle the exception 
				print(e)
				lan = input('\nPlease enter your desired language (2 letter code, e.g "en" = English, "hu" = Magyar, "de" = Deutsch):\n')
		
	except Exception as e:
		# if something happens, e.g. not online
		print('An error has occured. The language will remain English.')

	finally:
		print('Thank you for using the change language function.\n\n')
		return lan