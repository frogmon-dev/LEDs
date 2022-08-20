# frogmon.py
#-*- coding:utf-8 -*-

import sys
import io
import json
from frogmon.uRequest   import REQUEST
from frogmon.uGlobal    import GLOB
from frogmon.uCommon    import COM
from frogmon.uConfig    import CONF


config = CONF(COM.gHomeDir+COM.gSetupFile)

user_id = config.readConfig('SETUP', 'user_id', '')
dev_id  = config.readConfig('AGENT', 'id', '')

class pwinfo :
	e_temper = 0
	e_humidity = 0
	e_co  = 0.0
	e_no2 = 0.0
	e_so2 = 0.0
	e_o3  = 0.0
	e_pm10 = 0
	e_pm25 = 0
	e_pty = 0
	e_sky = 0
	e_wsd = 0.0	
	e_pty5 = 0
	e_sky5 = 0
	e_wsd5 = 0.0
	lstupdt = '200001010000'

class deviceinfo :
	dev_id   = ''
	user_id  = ''
	city     = ''
	station  = ''
	location = '0'
	version  = '0'
	teamviewer_id = ''
	lstupdt  = '200001010000'
	
def makeWeatherJsonFile(fileNM, data: pwinfo):
	#with open(fileNM, 'w', encoding='UTF-8-sig') as make_file:
	with open(fileNM, 'w', encoding='UTF-8') as make_file:
		dict = json.loads('{}')
		
		dict['e_temper']    = data.e_temper
		dict['e_humidity']  = data.e_humidity
		dict['e_co']        = data.e_co
		dict['e_no2']       = data.e_no2
		dict['e_so2']       = data.e_so2
		dict['e_o3']        = data.e_o3
		dict['e_pm10']      = data.e_pm10
		dict['e_pm25']      = data.e_pm25
		dict['e_pty']       = data.e_pty
		dict['e_sky']       = data.e_sky
		dict['e_wsd']       = data.e_wsd
		dict['e_pty5']      = data.e_pty5
		dict['e_sky5']      = data.e_sky5
		dict['e_wsd5']      = data.e_wsd5		
		dict['lstupdt']     = data.lstupdt
		
		json.dump(dict, make_file, indent="\t")
		#make_file.write(json.dumps(dict, ensure_ascii=False))
		
		print("New save File :" + fileNM)
		
def makeDeviceJsonFile(fileNM, data: deviceinfo):
	with open(fileNM, 'w', encoding='UTF-8') as make_file:
		dict = json.loads('{}')
		
		dict['DEV_ID']    = data.dev_id
		dict['USER_ID']   = data.user_id
		dict['CITY']      = data.city
		dict['STATION']   = data.station
		dict['LOCATION']  = data.location
		dict['VERSION']   = data.version
		dict['TEAMVIEWER']= data.teamviewer_id
		dict['LASTUPDT']  = data.lstupdt
		
		#json.dump(dict, make_file, indent="\t")
		make_file.write(json.dumps(dict, ensure_ascii=False, indent="\t"))
		print("New save File :" + fileNM)

GLOB.setUpdateTime()


def loadTeamviewerID():
	try:
		file = open(COM.gHomeDir+'teamviewerID.txt', 'r')
		strData = file.read()
		strData = strData.replace('TeamViewer ID:', '').rstrip("\n")
		strData = strData.replace(' ', '')
		strData = GLOB.escape_ansi(strData)
		
		return strData
	except Exception as e:
		print("error : %s" % e)
		return "-"


print('')
print('--------------------------------------------------')
print('**  Welcome to FROGMON corp.')
print("**  Let's make it together")
print("**  ")
print('**  USER = %s' % user_id)
print('**  PRODUCT = %s' % dev_id)
print('**  NOW times = %s' % COM.gstrYMDHMS)
print('**  location01 = %s' % config.readConfig('POLLUTION', 'location0', ''))
print('**  location02 = %s' % config.readConfig('POLLUTION', 'location1', ''))
print('**  location03 = %s' % config.readConfig('POLLUTION', 'location2', ''))
print('--------------------------------------------------')
print('')

chk = 0
for x in range(3):
	local_id  = config.readConfig('POLLUTION', 'location%s' % x, '')
	infoP = REQUEST.callPollution(local_id)
	infoW = REQUEST.callWeather(local_id)
	infoW5 = REQUEST.callWeatherAfter5(local_id)
	
	
	if (len(infoP) == 12 and len(infoW) == 8): 
		if (infoP[8] != '-' and infoP[9] != '-' and infoP[7] != '-'):
			chk = 1
			break

if (chk == 0):
	print('Data Load Error!')
	#exit()

print('Polluation raw Data-------------------------------')
print(infoP)
print('Weather raw Data----------------------------------')
print(infoW)
print('--------------------------------------------------')
mpwinfo = pwinfo

#mpwinfo.lstupdt    = str(infoP[0].replace('-', '').replace(':', '').replace('\ufeff\r\n\t\t\t', ''))
mpwinfo.lstupdt    = COM.gstrYMDHMS
mpwinfo.e_temper   = int(infoP[2].replace('-', '0'))
mpwinfo.e_humidity = int(infoP[3].replace('-', '0'))
mpwinfo.e_co       = float(infoP[4].replace('-', '0'))
mpwinfo.e_no2      = float(infoP[5].replace('-', '0'))
mpwinfo.e_so2      = float(infoP[6].replace('-', '0'))
mpwinfo.e_o3       = float(infoP[7].replace('-', '0'))
mpwinfo.e_pm10     = int(infoP[8].replace('-', '0'))
mpwinfo.e_pm25     = int(infoP[9].replace('-', '0'))

mpwinfo.e_pty      = int(infoW[0].replace('-', '0'))
mpwinfo.e_sky      = int(infoW[1].replace('-', '0'))
mpwinfo.e_wsd      = int(infoW[6].replace('-', '0'))

mpwinfo.e_pty5     = int(infoW5[0].replace('-', '0'))
mpwinfo.e_sky5     = int(infoW5[1].replace('-', '0'))
mpwinfo.e_wsd5     = int(infoW5[6].replace('-', '0'))

# make air.json file
makeWeatherJsonFile(COM.gJsonDir+'air.json', mpwinfo)

mDeviceInfo = deviceinfo
mDeviceInfo.dev_id   = config.readConfig('AGENT'    , 'id'       , '')
mDeviceInfo.user_id  = config.readConfig('SETUP'    , 'user_id'  , '')
mDeviceInfo.city     = config.readConfig('POLLUTION', 'city'     , '')
mDeviceInfo.station  = config.readConfig('POLLUTION', 'station'  , '')
mDeviceInfo.location = local_id
mDeviceInfo.version  = config.readConfig('SETUP'    , 'version'  , '')
mDeviceInfo.teamviewer_id = loadTeamviewerID()
mDeviceInfo.lstupdt  = config.readConfig('SETUP'    , 'lstworkdt', '')

# make device.json file
makeDeviceJsonFile(COM.gJsonDir+'device.json', mDeviceInfo)

print('Update Device Stat--------------------------------')
REQUEST.updateDIYs(mDeviceInfo.user_id, mDeviceInfo.dev_id)
print('--------------------------------------------------')

loadTeamviewerID()