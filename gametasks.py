# user score calling, update
import os
# get the current folder path
current_folder = os.path.dirname(os.path.abspath(__file__))

def get_user_score(user_name):
	# try to read txt, if doesnt exist, create it
	try:
		# use the current folder path to open or rename files
		file = open(os.path.join(current_folder, "user_scores.txt"), "r")
	
		for line in file:
			content = line.split(', ')
		
			if user_name == content[0]:
				file.close()
				return content[1]
	
		file.close()
		return '-1'
	
	except IOError:
		
		print('File not found. Creating file.')
		file = open(os.path.join(current_folder, "user_scores.txt"), "w")
		file.close()
		return '-1'

def update_user_score(new_user, user_name, score):
	# if new user, write name in file, else copy content to temp file to rewrite score
	
	if new_user == True:
		file = open(os.path.join(current_folder, "user_scores.txt"), 'a')
		file.write(user_name + ', ' + score + '\n')
		file.close()
	
	else:
		temp_file = open(os.path.join(current_folder, "user_scores.tmp"), 'w')
		file = open(os.path.join(current_folder, "user_scores.txt"), 'r')
		
		for line in file:
			content = line.split(', ')
			
			if user_name == content[0]:
				temp_file.write(user_name + ', ' + score + '\n')

			else:
				temp_file.write(line)
		
		file.close()
		temp_file.close()
		os.remove(os.path.join(current_folder, "user_scores.txt"))
		os.rename(os.path.join(current_folder, "user_scores.tmp"), os.path.join(current_folder, "user_scores.txt"))
		remove('user_scores.txt')
		rename('user_scores.tmp', 'user_scores.txt')

