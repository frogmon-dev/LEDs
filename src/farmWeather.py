# farmWeather.py
#-*- coding:utf-8 -*-

# 중복 실행 방지
from tendo import singleton
try:
	me = singleton.SingleInstance()
except :
	print("another process running!")
	exit()

#프로그램 시작
from frogmon.uCommon   import COM
from frogmon.uGlobal   import GLOB
from frogmon.uLogger   import LOG
from frogmon.uRequest  import REQUEST

configFileNM = COM.gHomeDir+COM.gSetupFile

user_id = GLOB.readConfig(configFileNM, 'SETUP', 'user_id', '')
dev_id  = GLOB.readConfig(configFileNM, 'AGENT', 'id', '')

GLOB.setUpdateTime()

print('')
print('--------------------------------------------------')
print('**  Welcome to FROGMON corp.')
print("**  Let's make it together")
print("**  ")
print('**  USER = %s' % user_id)
print('**  PRODUCT = %s' % dev_id)
print('**  NOW times = %s' % COM.gstrYMDHMS)
print('**  location01 = %s' % GLOB.readConfig(configFileNM, 'WEATHER', 'location0', ''))
print('**  location02 = %s' % GLOB.readConfig(configFileNM, 'WEATHER', 'location1', ''))
print('**  location03 = %s' % GLOB.readConfig(configFileNM, 'WEATHER', 'location2', ''))
print('--------------------------------------------------')
print('')

local_id  = GLOB.readConfig(configFileNM, 'WEATHER', 'location0', '')

if (local_id == ''):
	print("local id is empty")
	exit()

infoW = REQUEST.callWeather(local_id)

if (len(infoW) > 0) :
	GLOB.writeConfig(configFileNM, 'WEATHER', 't1h', infoW[4])
	GLOB.writeConfig(configFileNM, 'WEATHER', 'reh', infoW[2])
	GLOB.writeConfig(configFileNM, 'WEATHER', 'wsd', infoW[6])
	GLOB.writeConfig(configFileNM, 'WEATHER', 'pty', infoW[0])
	GLOB.writeConfig(configFileNM, 'WEATHER', 'sky', infoW[1])
	print("weather data get success!!")
