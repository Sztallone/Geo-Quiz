# create decorator to close program
import sys
def exit_on_minus_one(func):
	def wrapper(*args, **kwargs):
		# call the func function and get the return value
		value = func(*args, **kwargs)
		# check if the value is -1
		if value == '-1': 
			sys.exit('You cancelled the program.')
		else:
			return value
	return wrapper

