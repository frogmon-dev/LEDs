# uLogger.py
#-*- coding:utf-8 -*-

import sys
import logging
import logging.handlers
import sdnotify

from frogmon.uCommon import COM
from unidecode       import unidecode
from colorama import Fore, Back, Style

#logger instance create
logger        = logging.getLogger(__name__)
#logger formatter create
formatter     = logging.Formatter('[%(asctime)s] %(message)s')
#handler create (stream, file)
streamHandler = logging.StreamHandler()
fileHandler   = logging.FileHandler(COM.gLogDir + 'syslog_%s.log' % COM.gstrYMD)

#logger instance에 fomatter create
streamHandler.setFormatter(formatter)
fileHandler.setFormatter(formatter)

#logger instance에 handler create
logger.addHandler(streamHandler)
logger.addHandler(fileHandler)

#Log Level Setting
logger.setLevel(level=logging.DEBUG)

# Systemd Service Notifications - https://github.com/bb4242/sdnotify
sd_notifier = sdnotify.SystemdNotifier()

class LOG():
	def writeLn(msg):
		logger.debug(msg)