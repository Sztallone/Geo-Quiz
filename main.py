from file_handler import FileHandler, CountryData, EUData, CityData
from question_maker import generate_question, print_choices_get_answer
from gametasks import get_user_score, update_user_score
import sys
from decorators import trnslate_func, exit_on_minus_one, print_translate
from language_select import change_language

try:
	# choose lang
	lan = change_language()

	# create function to use decors on input(). print() gets translated in decorators.py
	@trnslate_func(lan)	# translator decorator
	@exit_on_minus_one # exiter
	def input_translate(prompt):
		user_input = input(prompt)
		return user_input
	
	@trnslate_func(lan)	# translator decorator with no exit
	def input_translate_noexit(prompt):
		user_input = input(prompt)
		return user_input
	
	print_translate('\nWelcome to the Geo-Quiz game! In this game you will have to answer geographical questions about countries. \nEach correct answer gives you one mark.\nNo mark is deducted for wrong answers.\nType (-1) to exit whenever you like.\n', lan)

	print_translate('Processing Data.\n', lan)
	# Load csvs into DF, merge
	try:
		country_df = CountryData.read_file('country_data')
		eu_df = EUData.read_file('eu_members')
		city_df = CityData.read_file('worldcities')

		full_data = FileHandler.merge_data(country_df, eu_df, city_df)

	except OSError:
		sys.exit('Error during file handling!')
	else:
		print_translate('Data loaded.\n', lan)

	# get username, score	
	user_name = input_translate('Hello! Please enter your name:\n')

	while True:
		if user_name == '':
			user_name = input_translate('Please enter your name: ')
		else:
			break

	score = int(get_user_score(user_name))

	if score == -1:
		new_user = True
		score = 0
	else:
		new_user = False
	
	print_translate(f'Hi {user_name}, welcome. Your score is: {score}.\nPlease select a topic for your questions.', lan)

	user_choice = 0
	
	# game goes on until player choice
	while user_choice != '-1':
		#prompt user to select Feature
		
		input_feature = input_translate('\nChoose one of the following: \nLandmass (1) | Population (2) | Continent (3) | EU membership (4) | Capital (5) | Latitude of Capital (6) | Population of Capital (7) \n')

		valid_feature_answers = list(range(1, 8))
		
		while True:
			try:
				int(input_feature)
				try:
					if int(input_feature) in valid_feature_answers:
						input_feature = int(input_feature)
						break
					else:
						print_translate('You did not enter a valid choice. Please try again.', lan)
						input_feature = input_translate('Please write (1), (2), (3), (4), (5), (6) or (7): \n')
				except:
						print_translate('You did not enter a valid choice. Please try again.', lan)
						input_feature = input_translate('Please write (1), (2), (3), (4), (5), (6) or (7): \n')
			except:
				print_translate('Not a valid number!', lan)
				input_feature = input_translate('\nChoose one of the following: \nLandmass (1) | Population (2) | Continent (3) | EU membership (4) | Capital (5) | Latitude of Capital (6) | Population of Capital (7) \n')
		
		#prompt user for number of questions per game
		number_prompt = input_translate('How many questions do you want per game (1 to 10)?: \n')
	
		# accept only numbers and modify answer
		while True:
			try:
				no_of_questions = int(number_prompt)	
				if no_of_questions in range(1, 11):
					break
				else:
					if no_of_questions < 1:
						no_of_questions = 1
						print_translate('\nMinimum number of questions = 1', lan)
						print_translate('Hence, number of questions will be set to 1', lan)
						break
					elif no_of_questions > 10:
						no_of_questions = 10
						print_translate('\nMaximum number of questions = 10', lan)
						print_translate('Hence, number of questions will be set to 10', lan)
						break
			except:
				print_translate('Not a valid number!', lan)
				number_prompt = input_translate('How many questions do you want per game (1 to 10)?: \n')
			
		# Feature choices
		# pair integer userinput with col names
		col_names_dict = {}
		for i in valid_feature_answers:
			col_names_dict[i] = full_data.columns[i + 1]

		#display relevant questions based on user’s selection and update user score
		for i in range(no_of_questions):
			
			question, unit, value, feature = generate_question(full_data, col_names_dict[input_feature])

			# get player's answer and result
			answer_letter, player_answer = print_choices_get_answer(full_data, question, unit, value, feature, lan)

			if answer_letter == player_answer:
				print_translate('Answer is correct!', lan)
				score += 1
			else:
				print_translate(f'Answer is incorrect! The right answer is: {answer_letter}.', lan)
		
		#display updated score to user
		print_translate(f'Your current score : {score}', lan)
		#prompt user to enter a choice again and use it to update user_choice
		user_choice = input_translate_noexit('Press Enter to continue or (-1) to exit: ')
		if user_choice == '-1':
			print_translate('\n\nThank you for playing!\n', lan)
	
	#update the user’s score after he/she exits the program
	update_user_score(new_user, user_name, str(score))

except Exception as e:
	#inform users that an error has occurred and the program will
	print_translate('An unknown error has occured. The program will exit.', lan)
	print_translate('Error: ' + str(e), lan)
