# uConfig.py
# -*- coding: utf-8 -*-

from configparser import ConfigParser
from frogmon.uCommon import COM

# Load configuration file    
config = ConfigParser(delimiters=('=', ), inline_comment_prefixes=('#'))
config.optionxform = str

confFileNM = ''

class CONF():
	def __init__(self, filename):
		self.confFileNM = filename
	
	def readConfig(self, section, item, _def):
		try:
			config.read(self.confFileNM)
			return config[section].get(item, _def)
		except:
			print('section or item not found')
			return _def

	def readConfigBool(self, section, item, _def: bool):
		try:
			config.read(self.confFileNM)		
			return config[section].getboolean(item, _def)
		except:
			print('section or item not found')
			return _def

	def readConfigInt(self, section, item, _def: int):
		try:
			config.read(self.confFileNM)		
			return int(config[section].get(item, _def))
		except:
			print('section or item not found')
			return _def	

	def readConfigFile(self):
		try:
			config.read(self.confFileNM)		
		except:
			print('config file load error')
			return _def	

	def writeConfig(self, section, item, val):
		config.set(section, item.lower(), val)
	
	def saveConfig(self):
		with open(self.confFileNM, 'w') as f:
			config.write(f)