# uRequest.py

#-*- coding:utf-8 -*-

import requests
import urllib.parse

from datetime import datetime, timedelta

from frogmon.uCommon import COM
from frogmon.uGlobal import GLOB
from frogmon.uConfig import CONF
from frogmon.uLogger import LOG
from frogmon.uXml    import XMLPaser

class REQUEST():	
	def updateDIYs(user_id, dev_id):
		if user_id == 'empty' or dev_id == 'empty' :
			LOG.writeLn("user_id or dev_id is empty")
			exit()
			
		phpFileNm = "call_from_DIYs.php";
		
		fileName = COM.gJsonDir + 'device.json'
		
		f = open(fileName, 'r')
		data = f.read()
		print(data)
		f.close()

		url = 'https://frogmon.synology.me/smf_system/'
		url = '%s%s' % (url, phpFileNm)
		r = requests.post(url, data={'user_id': user_id, 'product_id': dev_id, 'status_json': data})
		#print(r.url)
		if (XMLPaser.getHeader(r.content) != 0):
			LOG.writeLn("sendModuleStat send Error ")	
		else:
			actionJson = XMLPaser.decodeAction(r.content)
			if actionJson == '':
				print('no Actions')
			else :
				GLOB.saveJsonData(COM.gJsonDir+'action.json', '0x11', actionJson)

	def callPollution(local_id):
		if local_id == '' or local_id == 'empty' :
			LOG.writeLn("[callPollution] local_id is empty")	
			exit()
			
		phpFileNm = "seindex.php";
		
		url = 'http://58.229.176.179/'
		url = "%s%s?position=%s" % (url, phpFileNm, local_id)
		
		try:
			r = requests.get(url=url, timeout=3)
			#print(r.url)
			#print('--------------------')
			s = r.content.decode("UTF-8")
			s = s.replace('<h1>', '')
			s = s.replace('</h1>', '')
			s = s.replace(' ', '')
			
			rc = s.split(',')
			return rc
		except:
			LOG.writeLn("[callPollution] Error : %s" % r.url)
			
	def callWeather(local_id):
		if local_id == '' or local_id == 'empty' :
			LOG.writeLn("[callWeather] local_id is empty")	
			exit()
			
		phpFileNm = "get_weather_info.php";
		
		#url = 'http://119.197.41.9/svr_api/'
		url = 'http://frogmon.synology.me/svr_api/'
		url = "%s%s?position=%s" % (url, phpFileNm, local_id)
		
		try:
			r = requests.get(url=url, timeout=3)
			#print(r.url)
			#print('--------------------')
			#s = r.content.decode("UTF-8").strip()
			#print(s)
			return XMLPaser.decodeWeather(r.content)
		except:
			LOG.writeLn("[callWeather] Error : %s" % r.url)
			
	
	def callCovid19():
			
		phpFileNm = "get_covid19_info.php";
		
		#url = 'http://119.197.41.9/svr_api/'
		url = 'http://frogmon.synology.me/svr_api/'
		url = "%s%s" % (url, phpFileNm)
		
		try:
			r = requests.get(url=url, timeout=3)
			#print(r.url)
			#print('--------------------')
			#s = r.content.decode("UTF-8").strip()
			#print(s)
			return XMLPaser.decodeCovid19(r.content)
		except:
			LOG.writeLn("[callCovid19] Error : %s" % r.url)
	
	def getNews():
			
		phpFileNm = "get_news_list.php";
		
		#url = 'http://119.197.41.9/svr_api/'
		url = 'http://frogmon.synology.me/svr_api/'
		url = "%s%s" % (url, phpFileNm)
		
		try:
			r = requests.get(url=url, timeout=3)
			return XMLPaser.decodeNews(r.content)
		except:
			LOG.writeLn("[getNews] Error : %s" % r.url)		
		
	
	def callWeatherAfter5(local_id):
		if local_id == '' or local_id == 'empty' :
			LOG.writeLn("[callWeather] local_id is empty")	
			exit()
			
		phpFileNm = "get_weather_after5_info.php";
		
		#url = 'http://119.197.41.9/svr_api/'
		url = 'http://frogmon.synology.me/svr_api/'
		url = "%s%s?position=%s" % (url, phpFileNm, local_id)
		
		try:
			r = requests.get(url=url, timeout=3)
			#print(r.url)
			#print('--------------------')
			#s = r.content.decode("UTF-8").strip()
			#print(s)
			return XMLPaser.decodeWeather(r.content)
		except:
			LOG.writeLn("[callWeatherAfter5] Error : %s" % r.url)
