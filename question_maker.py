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

def print_choices_get_answer(dataframe, question, unit, value, feature):
		
	choices = [value]

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
		
		# select correct index and match with answer letter
		answer_index = choices.index(value)

		answer_letter = 'ABCD'[answer_index]
		
		print(question) # choices comma separated if number
		if type(choices[0]) == str or feature == 'EU membership':
			print(f'A) {choices[0]:} {unit}')
			print(f'B) {choices[1]:} {unit}')
			print(f'C) {choices[2]:} {unit}')
			print(f'D) {choices[3]:} {unit}')
		else:
			print(f'A) {choices[0]:,} {unit}')
			print(f'B) {choices[1]:,} {unit}')
			print(f'C) {choices[2]:,} {unit}')
			print(f'D) {choices[3]:,} {unit}')
		
		# check player answers
		while True:
			player_answer = input('\nEnter your answer: ').upper()
			if player_answer in ['A', 'B', 'C', 'D']:
				break
			else:
				print('Not a valid answer!')

	else:
		choices = ['Northern', 'Southern']

		if value > 0:
			answer_letter = 'A'
		else:
			answer_letter = 'B'

		print(question)
		print(f'A) {choices[0]}')
		print(f'B) {choices[1]}')        
	
		while True:
			player_answer = input('\nEnter your answer: ').upper()
			if player_answer in ['A', 'B']:
				break
			else:
				print('Not a valid answer!')

	return answer_letter, player_answer
		
