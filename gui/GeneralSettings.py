import sys, os, json
from time import sleep
from os.path import join, dirname, abspath

from qtpy import uic
from qtpy.QtCore import Slot, QThread, Signal, Qt
from qtpy.QtWidgets import QApplication, QDialog, QListWidgetItem
from tmdbv3api.tmdb import TMDb

import qtmodern.styles
import qtmodern.windows

from guiConfig import guiConfig, settingFolder
_UI = join(dirname(abspath(__file__)), 'GeneralSettings.ui')

class GeneralSettingsWindow(QDialog):

    __langFile__  = settingFolder + 'langs.json'
    __langs__     = None

    def __init__(self):
        self.__langs__ = dict()

        QDialog.__init__(self)
        uic.loadUi(_UI, self)
        self.loadLanguages()
        self.loadIgnoreList()

        self.txtLang.textChanged[str].connect(self.actualizeLangByText)
        self.cbxLang.currentIndexChanged.connect(self.actualizeLangByBox)
        self.btnIgnoreAdd.clicked.connect(self.ignoreAdd)   
        self.btnIgnoreRemove.clicked.connect(self.ignoreRemove)  
        self.buttonBox.accepted.connect(self.accepted) 

        self.txtLang.setText(guiConfig["language"])
        self.chkOverwrite.setChecked(bool(guiConfig["overwrite_files"]))

    def accepted(self):
        ignores = list()
        for i in range(self.lstIgnore.count()):
            ignores.append(self.lstIgnore.item(i).text())
        guiConfig["ignore_pattern"]  = ignores
        guiConfig["overwrite_files"] = self.chkOverwrite.isChecked()
        guiConfig["language"]        = self.txtLang.text()
        guiConfig.saveSettings()

    def loadLanguages(self):
        langs = list()
        try:
            with open(self.__langFile__, "r") as readFile:
                langs = json.load(readFile)
        except:
            langs = TMDb()._call("/configuration/languages", "")
            with open(self.__langFile__, "w") as writeFile:
                json.dump(langs, writeFile, indent=4)

        for lang in langs:
            code = str(lang["iso_639_1"])
            name = lang["english_name"]
            self.__langs__[name] = code

        self.cbxLang.addItem('Invalid')
        self.cbxLang.addItems(sorted(self.__langs__.keys()))
    
    def actualizeLangByText(self):
        self.cbxLang.currentIndexChanged.disconnect()
        searchCode = self.txtLang.text().lower()
        for name, code in self.__langs__.items():
            if code == searchCode:
                self.cbxLang.setCurrentText(name)
                self.cbxLang.currentIndexChanged.connect(self.actualizeLangByBox)
                return
        
        self.cbxLang.setCurrentIndex(0)
        self.cbxLang.currentIndexChanged.connect(self.actualizeLangByBox)

    def actualizeLangByBox(self, i):
        self.txtLang.textChanged[str].disconnect()
        self.txtLang.setText(self.__langs__[self.cbxLang.currentText()])
        self.txtLang.textChanged[str].connect(self.actualizeLangByText)

    def __createListItem__(self, text : str):
        item = QListWidgetItem(text)
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        return item

    def loadIgnoreList(self):
        for ignore in guiConfig["ignore_pattern"]:
            self.lstIgnore.addItem(self.__createListItem__(ignore))

    def ignoreAdd(self):
        item = self.__createListItem__('pattern')
        self.lstIgnore.addItem(item)
        self.lstIgnore.editItem(item)
    
    def ignoreRemove(self):
        items = self.lstIgnore.selectedItems()
        for item in items:
            self.lstIgnore.takeItem(self.lstIgnore.row(item))
        