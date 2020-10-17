import os, json
from os.path import expanduser

settingFolder = expanduser("~") + '/.FileSort/'
settingFile   = settingFolder + 'settings.json'

GuiConfigDefault = {
    "show_output_format" : "./%n (%y)/Season %0s/%n (%y) - S%0sE%0e - %t.%x",
    "movie_output_format" : "%t (%y)/%t (%y).%x",
    "language" : "en",
    "overwrite_files" : True,
    "ignore_pattern": ["*.nfo", "*.jpg", "*.htm", "*.html", "*.url", '*.txt', "*.png", "*sample*", "*proof*", ".DS_Store"]
}

class GuiConfig(dict):
    def __init__(self):
        self.__dict__ = GuiConfigDefault
        self.loadSettings()

    def saveSettings(self):
        if not os.path.exists(settingFolder):
            os.makedirs(settingFolder)

        with open(settingFile, "w") as writeFile:
            json.dump(self.__dict__, writeFile, indent=4)

    def loadSettings(self):
        if not os.path.exists(settingFile):
            return

        try:
            with open(settingFile, "r") as readFile:
                self.__dict__ = json.load(readFile)
        except:
            return
    
    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__dict__[key] = value
    
    def __len__(self):
        return self.__dict__.__len__()

guiConfig = GuiConfig()