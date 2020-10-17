import sys
from time import sleep
from os.path import join, dirname, abspath

from qtpy import uic
from qtpy.QtCore import Slot, QThread, Signal
from qtpy.QtWidgets import QApplication, QDialog

import qtmodern.styles
import qtmodern.windows

from movieMatcher import MovieMatcher
from guiConfig import guiConfig
_UI = join(dirname(abspath(__file__)), 'MovieSettings.ui')

class MovieSettingsWindow(QDialog):

    __movieMatcher__ = MovieMatcher('./')

    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi(_UI, self)  # Load the ui into self    
        self.actualizePreview()
        self.txtMSOutFormat.textChanged[str].connect(self.actualizePreview)
        self.txtMSOutFormat.setText(guiConfig['movie_output_format'])
        self.buttonBox.accepted.connect(self.accepted)

    def actualizePreview(self):
        self.__movieMatcher__.outputFormat = self.txtMSOutFormat.text()
        self.txtMSPreview.setText(
            self.__movieMatcher__.createOutputFile(
                'Iron Man 2', 2010, 'mp4'))
    
    def accepted(self):
        guiConfig['movie_output_format'] = self.txtMSOutFormat.text()
        guiConfig.saveSettings()
