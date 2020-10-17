import sys
from os.path import join, dirname, abspath

from qtpy import uic
from qtpy.QtCore import Slot, QThread, Signal
from qtpy.QtWidgets import QApplication, QMainWindow, QMessageBox, QTreeWidgetItem, QTableView, QHeaderView

import qtmodern.styles
import qtmodern.windows

from MovieSettings import MovieSettingsWindow
from ShowSettings import ShowSettingsWindow
from GeneralSettings import GeneralSettingsWindow

_UI = join(dirname(abspath(__file__)), 'MainWindow.ui')

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi(_UI, self)  # Load the ui into self

        self.actionLight.triggered.connect(self.lightTheme)
        self.actionDark.triggered.connect(self.darkTheme)
        self.actionMovie_Settings.triggered.connect(self.openMovieSettings)
        self.actionShow_Settings.triggered.connect(self.openShowSettings)
        self.actionGeneral_Settings.triggered.connect(self.openGeneralSettings)
        self.actionExit.triggered.connect(self.close)

        self.tableShowOutput.horizontalHeader().setVisible(True)
        self.tableShowOutput.verticalHeader().setVisible(True)
        self.tableShowInput.horizontalHeader().setVisible(True)
        self.tableShowInput.verticalHeader().setVisible(True)
        self.tableMovieOutput.horizontalHeader().setVisible(True)
        self.tableMovieOutput.verticalHeader().setVisible(True)
        self.tableMovieInput.horizontalHeader().setVisible(True)
        self.tableMovieInput.verticalHeader().setVisible(True)

    def update_progress(self, progress):
        self.progressBar.setValue(progress)

    def lightTheme(self):
        qtmodern.styles.light(QApplication.instance())

    def darkTheme(self):
        qtmodern.styles.dark(QApplication.instance())
    
    def openMovieSettings(self):
        mw = qtmodern.windows.ModernWindow(MovieSettingsWindow())
        mw.show()
    
    def openShowSettings(self):
        mw = qtmodern.windows.ModernWindow(ShowSettingsWindow())
        mw.show()

    def openGeneralSettings(self):
        mw = qtmodern.windows.ModernWindow(GeneralSettingsWindow())
        mw.show()
