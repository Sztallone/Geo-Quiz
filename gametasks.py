# user score calling, update

def get_user_score(user_name):
	# try to read txt, if doesnt exist, create it
	try:
		file = open('user_scores.txt', 'r')
	
		for line in file:
			content = line.split(', ')
		
			if user_name == content[0]:
				file.close()
				return content[1]
	
		file.close()
		return '-1'
	
	except IOError:
		
		print('File not found. Creating file.')
		file = open('user_scores.txt', 'w')
		file.close()
		return '-1'

def update_user_score(new_user, user_name, score):
	from os import remove, rename 
	# if new user, write name in file, else copy content to temp file to rewrite score
	
	if new_user == True:
		file = open('user_scores.txt', 'a')
		file.write(user_name + ', ' + score + '\n')
		file.close()
	
	else:
		temp_file = open('user_scores.tmp', 'w')
		file = open('user_scores.txt', 'r')
		
		for line in file:
			content = line.split(', ')
			
			if user_name == content[0]:
				temp_file.write(user_name + ', ' + score + '\n')

			else:
				temp_file.write(line)
		
		file.close()
		temp_file.close()
		remove('user_scores.txt')
		rename('user_scores.tmp', 'user_scores.txt')

