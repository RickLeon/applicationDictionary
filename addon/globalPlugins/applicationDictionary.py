#Application Dictionary addon for NVDA
#This file is covered by the GNU General Public License.
#See the file COPYING.txt for more details.
#Copyright (C) 2018 Ricardo Leonarczyk <ricardo.leonarczyk95@gmail.com>

import api
import globalPluginHandler
import gui
import speechDictHandler
import os
from speechDictHandler import speechDictsPath
import addonHandler
addonHandler.initTranslation()
try:
	from globalCommands import SCRCAT_CONFIG
except:
	SCRCAT_CONFIG = None

def getAppName():
	return api.getForegroundObject().appModule.appName

def getDictFilePath(appName):
	return os.path.join(speechDictsPath, appName + ".dic")

def loadEmptyDicts():
	return dict([(f[:-4], None) for f in os.listdir(speechDictsPath) if os.path.isfile(os.path.join(speechDictsPath, f)) and f.endswith(".dic")])

def getDict(appName):
	dict = None
	if appName in dicts:
		dictFilePath = getDictFilePath(appName)
		if dicts[appName] is None:
			dict = speechDictHandler.SpeechDict()
			dict.load(dictFilePath)
			dicts[appName] = dict
		else:
			dict = dicts[appName]
	return dict

dicts = loadEmptyDicts()


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	__currentDict = None
	__currentAppName = None

	def event_foreground(self, obj, nextHandler):
		appName = getAppName()
		if self.__currentAppName is None or self.__currentAppName != appName:
			self.__currentAppName = appName
			dict = getDict(appName)
			self.__setCurrentDict(dict)
		nextHandler()

	def script_editDict(self, gesture):
		appName = getAppName()
		dict = getDict(appName)
		if dict is None:
			dictFilePath = getDictFilePath(appName)
			open(dictFilePath, "a").close()
			dict = speechDictHandler.SpeechDict()
			dict.load(dictFilePath)
			dicts[appName] = dict
# Translators: title of application dictionary dialog.
		title = _("Dictionary for {arg0}").format(arg0=appName)
		gui.mainFrame._popupSettingsDialog(gui.DictionaryDialog, title, dict)
	script_editDict.category = SCRCAT_CONFIG
# Translators: Message presented in input help mode.
	script_editDict.__doc__ = _("Shows the application-specific dictionary dialog")

# Temp dictionary use taken from emoticons add-on
	def __setCurrentDict(self, dict):
		if self.__currentDict is not None:
			for e in self.__currentDict: speechDictHandler.dictionaries["temp"].remove(e)
		self.__currentDict = dict
		if self.__currentDict is not None:
			speechDictHandler.dictionaries["temp"].extend(self.__currentDict)

	__gestures = {
		"kb:NVDA+Shift+p": "editDict"
}
