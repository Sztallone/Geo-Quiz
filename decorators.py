# create decorator to close program
import sys

def exit_on_minus_one(func):
	def wrapper(*args, **kwargs):
		# call the func function and get the return value
		value = func(*args, **kwargs)
		# check if the value is -1
		if value == '-1':
			print('You cancelled the program.') 
			sys.exit()
		else:
			return value
	return wrapper

# create decorator to translate

from googletrans import Translator
import functools
import re

# trns object
translator = Translator()

def trnslate_func(lan = 'en'):
# translates the string function arguments of a function to a given language
	# outer wrapper
	def decorator_trnslate(func_arg):
		@functools.wraps(func_arg) # save func info
		def wrapper(*args, **kwargs):
			translated_args = []
			translated_kwargs = {}
			
			# translator.translate strips the whitespace from the end of the string, we need to put it back with RE 
			# translate the input arguments to the desired language if str, else do nothing

			for arg in args:
				if isinstance(arg, str) and arg is not None:
					# search for whitespace chars, if None, return nothing 
					whitespace = re.search(r'\s*$', arg)
					if whitespace:
						whitespace = whitespace.group()
					else:
						whitespace = ''
					translated_args.append(translator.translate(arg, dest = lan).text + whitespace)
				else:
					translated_args.append(arg)
			
			for key, value in kwargs.items():
				if isinstance(value, str) and value is not None:
					whitespace = re.search(r'\s*$', value)
					if whitespace:
						whitespace = whitespace.group()
					else:
						whitespace = ''
					translated_kwargs[key] = translator.translate(value, dest = lan).text + whitespace
				else:
					translated_kwargs[key] = value
			# get the result with translated args
			result = func_arg(*translated_args, **translated_kwargs)
			return result
		return wrapper
	return decorator_trnslate

# func to trans strings
def simple_translate(string, lan = 'en'):
	translated_str = translator.translate(string, dest=lan).text
	return translated_str

# func to trans print
def print_translate(string, lan = 'en'):
	translated_str = translator.translate(string, dest=lan).text
	print(translated_str)
