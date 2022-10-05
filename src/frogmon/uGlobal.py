#uGlobal.py

import os
import re

from unidecode       import unidecode
from datetime import datetime, timedelta

from frogmon.uCommon import COM

class GLOB:
	def __init__(self):
		print('init')

  ## 파일명 검색
	def getJsonFile(dirname, word):
		filenames = os.listdir(dirname)
		rc = []

		for filename in filenames:
			full_filename = os.path.join(dirname, filename)
			if word in full_filename:
				if ('save' not in full_filename) :
					rc.append(full_filename)
		return rc	

	def loadJsonFile(fileName: str):
		f = open(fileName, 'r')
		data = ''.join(f.read().split())
		f.close()
		return data

	def setUpdateTime():
		COM.gNOW  = datetime.now()
		COM.gYYYY = COM.gNOW.strftime('%Y')
		COM.gMM   = COM.gNOW.strftime('%m')
		COM.gDD   = COM.gNOW.strftime('%d')
		COM.gHH   = COM.gNOW.strftime('%H')
		COM.gNN   = COM.gNOW.strftime('%M')
		COM.gSS   = COM.gNOW.strftime('%S')
		COM.gstrYMD = COM.gNOW.strftime('%Y%m%d')
		COM.gstrYMDHMS = COM.gNOW.strftime('%Y%m%d%H%M%S')
		COM.gstrDATE = COM.gNOW.strftime('%Y-%m-%d %H:%M:%S')
		
		COM.gII = COM.gNOW.strftime('%I')
		COM.gAPM  = COM.gNOW.strftime('%p')

	def betweenNow(strTm: str):
		convert_date = datetime.strptime(strTm, '%Y%m%d%H%M%S')
		now = datetime.now()
		return (now - convert_date).seconds
		

	def remoteFileFind(path):    
		file_list = os.listdir(path)
		file_list_remote = [file for file in file_list if file.startswith("remote_")]
		return file_list_remote
		
	# Making CSV function
	def makeCSVFile(data, fileName):
		print('fileName ='+fileName)
		print(data)
		if os.path.isfile(fileName) :
			f = open(fileName,'a', newline='')
			wr = csv.writer(f)
			wr.writerow(data)
			f.close()
		else :
			f = open(fileName,'w', newline='')
			wr = csv.writer(f)
			aRow = 'hhnnss', 'temp', 'humi', 'light', 'outTemp'
			wr.writerow(aRow)
			wr.writerow(data)
			f.close()

	# Identifier cleanup
	def clean_identifier(name):
		clean = name.strip()
		for this, that in [[' ', '-'], ['ä', 'ae'], ['Ä', 'Ae'], ['ö', 'oe'], ['Ö', 'Oe'], ['ü', 'ue'], ['Ü', 'Ue'], ['ß', 'ss']]:
			clean = clean.replace(this, that)
		clean = unidecode(clean)
		return clean
		
	def isMacAddress(mac):
		return re.match("[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}", mac.lower())

	def saveJsonData(fileName, opcode, data: str):
		if data:
			afterData = data.replace("'", "\"")
			dict = json.loads(afterData)
			with open(fileName, 'w', encoding='utf-8') as make_file:
				json.dump(dict, make_file, indent="\t")

	def escape_ansi(line):
		ansi_escape = re.compile(r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]')
		return ansi_escape.sub('', line)