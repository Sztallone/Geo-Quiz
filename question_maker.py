import random

def generate_question(dataframe, feature):
	
	if feature not in dataframe.columns[1:]:
		return 'Invalid feature'
	
	# get rand subjects for q's
	subject = random.choice(list(dataframe['Name']))
	subject_city = random.choice(list(dataframe['Capital']))

	# get rand non-0 row for EU member
	#random_eu_member = dataframe[dataframe['EU membership'] != 0].sample()['Name'].values[0] 
	random_eu_member = dataframe[dataframe['EU membership'] != 0].sample(n=1)['Name'].item() 

	if feature == 'Population':
		question = f'What is the population of {subject}?'
		unit = ''
		value = dataframe[dataframe['Name'] == subject]['Population'].values[0]
	elif feature == 'Landmass':
		question = f'What is the land mass of {subject} in square kilometers?'
		unit = 'km^2'
		value = dataframe[dataframe['Name'] == subject]['Landmass'].values[0]
	elif feature == 'Continent':
		question = f'On which continent is {subject} located?'
		unit = ''
		value = dataframe[dataframe['Name'] == subject]['Continent'].values[0]
	elif feature == 'Latitude of Capital':
		question = f'In which hemisphere is the capital of {subject} located?'
		unit = ''
		value = dataframe[dataframe['Name'] == subject]['Latitude of Capital'].values[0]
	elif feature == 'Capital':
		question = f'What is the capital city of {subject}?'
		unit = ''
		value = dataframe[dataframe['Name'] == subject]['Capital'].values[0]
	elif feature == 'Population of Capital':
		question = f'What is the population of {subject_city}?'
		unit = ''
		value = dataframe[dataframe['Capital'] == subject_city]['Population of Capital'].values[0]
	elif feature == 'EU membership':
		question = f'In which year did {random_eu_member} join the European Union?'
		unit = ''
		value = dataframe[dataframe['Name'] == random_eu_member]['EU membership'].values[0]
	
	return question, unit, value, feature

from decorators import trnslate_func, exit_on_minus_one, simple_translate, print_translate

def print_choices_get_answer(dataframe, question, unit, value, feature, lan = 'en'):
	import sys

	choices = [value]

	# set up decos inside function
	@trnslate_func(lan)	# translator decorator
	@exit_on_minus_one # exiter
	def input_translate(prompt):
		user_input = input(prompt)
		return user_input

	# build up choices w rand 
	if feature != 'Latitude of Capital':
		if feature == 'EU membership':
			while len(choices) < 4:
				# pick from values of rows that are not 0 in EU membership. to_list is reliable with NA
				#choice = random.choice(list(dataframe[dataframe['EU membership'] != 0]['EU membership']))
				choice = random.choice(dataframe[dataframe['EU membership'] != 0]['EU membership'].to_list())
				if choice not in choices:
					choices.append(choice)
		else:
			while len(choices) < 4:
				choice = random.choice(list(dataframe[feature]))

				if choice not in choices:
					choices.append(choice)
		
		random.shuffle(choices)

		if lan != 'en':
		# make translated copy of choices for exact match later
			translated_choices = [simple_translate(str(choice), lan) for choice in choices]

		# select correct index and match with answer letter
		answer_index = choices.index(value)

		answer_letter = 'ABCD'[answer_index]
			
		print_translate(question, lan) # choices comma separated if number
		if type(choices[0]) == str or feature == 'EU membership':
			print_translate(f'A) {choices[0]:} {unit}', lan)
			print_translate(f'B) {choices[1]:} {unit}', lan)
			print_translate(f'C) {choices[2]:} {unit}', lan)
			print_translate(f'D) {choices[3]:} {unit}', lan)
		else:
			print_translate(f'A) {choices[0]:,} {unit}', lan)
			print_translate(f'B) {choices[1]:,} {unit}', lan)
			print_translate(f'C) {choices[2]:,} {unit}', lan)
			print_translate(f'D) {choices[3]:,} {unit}', lan)

		# check player answers
		while True:
			player_answer = input_translate('\nEnter your answer: ').upper()
			
			# create cap_choices to check exact answers. if not EN, use translated versions of choices to pair
			if lan == 'en':
				capital_choices = [str(x).upper() for x in choices]
			else:
				capital_choices = [str(x).upper() for x in translated_choices]

			if player_answer in ['A', 'B', 'C', 'D']:
				break
			# check if player types in the answer, designate w correct letters
			elif player_answer in capital_choices:
				player_answer_index = capital_choices.index(player_answer)
				player_answer = 'ABCD'[player_answer_index]
				break
			elif player_answer == '-1':
				sys.exit('You cancelled the program.')
			else:
				print_translate('Not a valid answer!', lan)

	else:
		# latitude question
		choices = ['Northern', 'Southern']
		
		if lan != 'en':
			translated_choices = [simple_translate('Northern', lan), simple_translate('Southern', lan)]

		if value > 0:
			answer_letter = 'A'
		else:
			answer_letter = 'B'

		print_translate(question, lan)
		print_translate(f'A) {choices[0]}', lan)
		print_translate(f'B) {choices[1]}', lan)        
	
		while True:
			player_answer = input_translate('\nEnter your answer: ').upper()
			if lan == 'en':
				capital_choices = [str(x).upper() for x in choices]
			else:
				capital_choices = [str(x).upper() for x in translated_choices]

			if player_answer in ['A', 'B']:
				break
			elif player_answer in capital_choices:
				player_answer_index = capital_choices.index(player_answer)
				player_answer = 'AB'[player_answer_index]
				break
			# exit handled by decorator
			# elif player_answer == '-1':
			# 	sys.exit('You cancelled the program.')
			else:
				print_translate('Not a valid answer!', lan)

	return answer_letter, player_answer
