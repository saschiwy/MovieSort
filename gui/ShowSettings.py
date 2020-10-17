import sys
from os.path import join, dirname, abspath

from qtpy import uic
from qtpy.QtCore import Slot, QThread, Signal
from qtpy.QtWidgets import QApplication, QDialog

import qtmodern.styles
import qtmodern.windows

from episodeMatcher import EpisodeMatcher
from guiConfig import guiConfig
_UI = join(dirname(abspath(__file__)), 'ShowSettings.ui')

class ShowSettingsWindow(QDialog):

    __showMatcher__ = EpisodeMatcher()

    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi(_UI, self)  # Load the ui into self    
        self.actualizePreview()
        self.txtMSOutFormat.textChanged[str].connect(self.actualizePreview)
        self.txtMSOutFormat.setText(guiConfig['show_output_format'])
        self.buttonBox.accepted.connect(self.accepted)

    def actualizePreview(self):
        self.__showMatcher__.outputFormat = self.txtMSOutFormat.text()
        self.txtMSPreview.setText(
            self.__showMatcher__.createOutputFile(
                showName = 'The Boys', 
                episodeTitle = 'We Gotta Go Now',
                seasonNumber = 2,
                episodeNumber = 5,
                year = 2019,
                extension = 'mp4'))
    
    def accepted(self):
        guiConfig['show_output_format'] = self.txtMSOutFormat.text()
        guiConfig.saveSettings()
