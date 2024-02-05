from file_handler import FileHandler, CountryData, EUData, CityData
from question_maker import generate_question, print_choices_get_answer
from gametasks import get_user_score, update_user_score
import sys
from decorators import exit_on_minus_one


try:
	print('\nWelcome to the Geo-Quiz game! In this game you will have to answer geographical questions about countries. \nEach correct answer gives you one mark.\nNo mark is deducted for wrong answers.\nType (-1) to exit whenever.\n')

	print('Processing Data.\n')
	# Load csvs into DF, merge
	try:
		country_df = CountryData.read_file('country_data')
		eu_df = EUData.read_file('eu_members')
		city_df = CityData.read_file('worldcities')

		full_data = FileHandler.merge_data(country_df, eu_df, city_df)

	except OSError:
		sys.exit('Error during file handling!')
	else:
		print('Data loaded.\n')
	
	# create function to use decor on input()
	@exit_on_minus_one
	def get_input(user_instruction):
		# func to get the value of an input func
		user_input = input(user_instruction)
		return user_input

	# get username, score	
	user_name = get_input('Hello! Please enter your name: ')

	while True:
		if user_name == '':
			user_name = get_input('Please enter your name: ')
		else:
			break

	score = int(get_user_score(user_name))

	if score == -1:
		new_user = True
		score = 0
	else:
		new_user = False
	
	print(f'Hi {user_name}, welcome. Your score is: {score}.\nPlease select a topic for your questions.')

	user_choice = 0
	
	# game goes on until player choice
	while user_choice != '-1':
		#prompt user to select Feature
		
		input_feature = get_input('\nChoose one of the following: \nLandmass (1) | Population (2) | Continent (3) | EU membership (4) | Capital (5) | Latitude of Capital (6) | Population of Capital (7) \n')

		valid_feature_answers = list(range(1, 8))
		
		while True:
			try:
				int(input_feature)
				try:
					if int(input_feature) in valid_feature_answers:
						input_feature = int(input_feature)
						break
					else:
						print('You did not enter a valid choice. Please try again.')
						input_feature = get_input('Please write (1), (2), (3), (4), (5), (6) or (7): \n')
				except:
						print('You did not enter a valid choice. Please try again.')
						input_feature = get_input('Please write (1), (2), (3), (4), (5), (6) or (7): \n')
			except:
				print('Not a valid number!')
				input_feature = get_input('\nChoose one of the following: \nLandmass (1) | Population (2) | Continent (3) | EU membership (4) | Capital (5) | Latitude of Capital (6) | Population of Capital (7) \n')
		
		#prompt user for number of questions per game
		number_prompt = get_input('How many questions do you want per game (1 to 10)?: \n')
	
		# accept only numbers and modify answer
		while True:
			try:
				no_of_questions = int(number_prompt)	
				if no_of_questions in range(1, 11):
					break
				else:
					if no_of_questions < 1:
						no_of_questions = 1
						print('\nMinimum number of questions = 1')
						print('Hence, number of questions will be set to 1')
						break
					elif no_of_questions > 10:
						no_of_questions = 10
						print('\nMaximum number of questions = 10')
						print('Hence, number of questions will be set to 10')
						break
			except:
				print('Not a valid number!')
				number_prompt = get_input('How many questions do you want per game (1 to 10)?: \n')
			
		# Feature choices
		
		col_names_dict = {}
		for i in valid_feature_answers:
			col_names_dict[i] = full_data.columns[i + 1]

		#display relevant questions based on user’s selection and update user score
		for i in range(no_of_questions):
			
			question, unit, value, feature = generate_question(full_data, col_names_dict[input_feature])

			# get player's answer and result
			answer_letter, player_answer = print_choices_get_answer(full_data, question, unit, value, feature)

			if answer_letter == player_answer:
				print('\nAnswer is correct!\n')
				score += 1
			else:
				print(f'\nAnswer is incorrect! The right answer is: {answer_letter}.\n')
		
		#display updated score to user
		print(f'Your current score : {score}')
		#prompt user to enter a choice again and use it to update user_choice
		user_choice = input('Press Enter to continue or (-1) to exit: ')
		if user_choice == '-1':
			print('\n\nThank you for playing!\n')
	
	#update the user’s score after he/she exits the program
	update_user_score(new_user, user_name, str(score))

except Exception as e:
	#inform users that an error has occurred and the program will
	
	print('An unknown error has occured. The program will exit.')
	print('Error: ', e)


# another way to exit 
# except KeyboardInterrupt:
# 	print('\n\nThank you for playing!')

