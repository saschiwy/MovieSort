import sys, json, os
from time import sleep
from os.path import join, dirname, abspath

from qtpy.QtCore import Slot, QThread, Signal, Qt
from qtpy.QtWidgets import QApplication, QDialog, QListWidgetItem
from tmdbv3api.tmdb import TMDb

import qtmodern.styles
import qtmodern.windows

from .guiConfig import guiConfig, settingFolder
from .Ui_GeneralSettings import Ui_GerneralSettings as Ui_Settings

class GeneralSettingsWindow(QDialog):

    __langFile__  = settingFolder + 'langs.json'
    __langs__     = None

    def __init__(self):
        self.__langs__ = dict()
        QDialog.__init__(self)
        
        self.ui = Ui_Settings()
        self.ui.setupUi(self)

        self.loadLanguages()
        self.loadIgnoreList()

        self.ui.txtLang.textChanged[str].connect(self.actualizeLangByText)
        self.ui.cbxLang.currentIndexChanged.connect(self.actualizeLangByBox)
        self.ui.btnIgnoreAdd.clicked.connect(self.ignoreAdd)   
        self.ui.btnIgnoreRemove.clicked.connect(self.ignoreRemove)  
        self.ui.buttonBox.accepted.connect(self.accepted) 

        self.ui.txtLang.setText(guiConfig["language"])
        self.ui.chkOverwrite.setChecked(bool(guiConfig["overwrite_files"]))

    def accepted(self):
        ignores = list()
        for i in range(self.ui.lstIgnore.count()):
            ignores.append(self.ui.lstIgnore.item(i).text())
        guiConfig["ignore_pattern"]  = ignores
        guiConfig["overwrite_files"] = self.ui.chkOverwrite.isChecked()
        guiConfig["language"]        = self.ui.txtLang.text()
        TMDb().language = guiConfig['language']
        guiConfig.saveSettings()

    def loadLanguages(self):
        langs = list()
        try:
            with open(self.__langFile__, "r") as readFile:
                langs = json.load(readFile)
        except:
            langs = TMDb()._call("/configuration/languages", "")
            
            if not os.path.exists(settingFolder):
                os.makedirs(settingFolder)

            with open(self.__langFile__, "w") as writeFile:
                json.dump(langs, writeFile, indent=4)

        for lang in langs:
            code = str(lang["iso_639_1"])
            name = lang["english_name"]
            self.__langs__[name] = code

        self.ui.cbxLang.addItem('Invalid')
        self.ui.cbxLang.addItems(sorted(self.__langs__.keys()))
    
    def actualizeLangByText(self):
        self.ui.cbxLang.currentIndexChanged.disconnect()
        searchCode = self.ui.txtLang.text().lower()
        for name, code in self.__langs__.items():
            if code == searchCode:
                self.ui.cbxLang.setCurrentText(name)
                self.ui.cbxLang.currentIndexChanged.connect(self.actualizeLangByBox)
                return
        
        self.ui.cbxLang.setCurrentIndex(0)
        self.ui.cbxLang.currentIndexChanged.connect(self.actualizeLangByBox)

    def actualizeLangByBox(self, i):
        self.ui.txtLang.textChanged[str].disconnect()
        self.ui.txtLang.setText(self.__langs__[self.ui.cbxLang.currentText()])
        self.ui.txtLang.textChanged[str].connect(self.actualizeLangByText)

    def __createListItem__(self, text : str):
        item = QListWidgetItem(text)
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        return item

    def loadIgnoreList(self):
        for ignore in guiConfig["ignore_pattern"]:
            self.ui.lstIgnore.addItem(self.__createListItem__(ignore))

    def ignoreAdd(self):
        item = self.__createListItem__('pattern')
        self.ui.lstIgnore.addItem(item)
        self.ui.lstIgnore.editItem(item)
    
    def ignoreRemove(self):
        items = self.ui.lstIgnore.selectedItems()
        for item in items:
            self.ui.lstIgnore.takeItem(self.ui.lstIgnore.row(item))
        
