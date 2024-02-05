class FileHandler:
	def __init__(self, file_name):
		self.file_name = file_name

	def print_file_name(self):
		print('The file name is', self.file_name)

	@staticmethod
	def read_file(file_name, **kwargs):
	# Use pandas to read the CSV file and return a DataFrame. Can add arguments    
		import pandas as pd
		try:
			df = pd.read_csv(file_name + '.csv', **kwargs)
			return df
		except FileNotFoundError:
		# if FileNotFound, give error message and return None
			print('The file does not exist or the file name is wrong.')
			return None
		
	@staticmethod
	def merge_data(df1, df2, df3):
	# Merge dfs on matching columns. If not in EU, place 0
		import pandas as pd
		m = pd.merge(df1, df2, on=['Name', 'Code'], how='left').fillna(0)
		m = pd.merge(m, df3, on= 'Code', how='left')
		m = m.dropna()
		m = m.convert_dtypes()
		return m


class CountryData(FileHandler):
	def __init__(self, file_name, country):
		super().__init__(file_name)
		self.country = country

	def print_country(self):
		print('The country is', self.country)

	@classmethod
	def read_file(cls, file_name):
	#Call the parent class's read_file, rename and convert data     
		df = super(CountryData, cls).read_file(file_name, usecols = ['name', 'ISO alpha 3', 'land area km', 'population', 'continent'],
											   dtype= {'land area km': float, 'population': int})
		df = df.set_axis(['Name', 'Code', 'Landmass', 'Population', 'Continent'], axis=1)
		df['Continent'] = df['Continent'].replace({'eu': 'Europe', 'na': 'North America', 'af': 'Africa', 'asia': 'Asia', 'sa': 'South America', 'cen': 'Central America', 'ocean': 'Oceania'})
		return df

	# str and reproduce to double check 
	def __str__(self):
		return f'CountryData(file_name={self.file_name}, country={self.country})'

	def __repr__(self):
		return f'CountryData({self.file_name!r}, {self.country!r})'


class EUData(FileHandler):
	def __init__(self, file_name, eu_member):
		super().__init__(file_name)
		self.eu_member = eu_member
	
	def print_eu_member(self):
		print('The EU member status is', self.eu_member)

	@classmethod
	def read_file(cls, file_name):
		# Call the parent class's read_file and convert to date, drop mm dd
		df = super(EUData, cls).read_file(file_name, parse_dates=['Member-Since'])
		df = df.rename(columns={'Member-Since': 'EU membership'})
		df['EU membership'] = df['EU membership'].dt.year
		return df

	def __str__(self):
		return f'EUData(file_name={self.file_name}, eu_member={self.eu_member})'

	def __repr__(self):
		return f'EUData({self.file_name!r}, {self.eu_member!r})'
	

class CityData(FileHandler):
	def __init__(self, file_name, city):
		super().__init__(file_name)
		self.city = city

	def print_city(self):
		print('The city is', self.city)

	@classmethod
	def read_file(cls, file_name):
		# Call the parent class's read_file and rename, drop cols, rows
		df = super(CityData, cls).read_file(file_name, usecols = ['city_ascii','lat','iso3','capital','population'])
		df = df.set_axis(['Capital', 'Latitude of Capital', 'Code', 'Capital_Type', 'Population of Capital'], axis=1)
		df = df[df['Capital_Type'] == 'primary']
		df = df.drop(['Capital_Type'], axis=1)
		df = df.dropna()
		df = df.convert_dtypes()
		return df
	
	def __str__(self):
		return f'CityData(file_name={self.file_name}, city={self.city})'

	def __repr__(self):
		return f'CityData({self.file_name!r}, {self.city!r})'

