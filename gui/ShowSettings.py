import sys
from os.path import join, dirname, abspath

from qtpy.QtCore import Slot, QThread, Signal
from qtpy.QtWidgets import QApplication, QDialog

import qtmodern.styles
import qtmodern.windows

from episodeMatcher import EpisodeMatcher
from guiConfig import guiConfig
from Ui_ShowSettings import Ui_Dialog as Ui_ShowSettings

class ShowSettingsWindow(QDialog):

    __showMatcher__ = EpisodeMatcher('./')

    def __init__(self):
        QDialog.__init__(self)

        self.ui = Ui_ShowSettings()
        self.ui.setupUi(self)

        self.actualizePreview()
        self.ui.txtMSOutFormat.textChanged[str].connect(self.actualizePreview)
        self.ui.txtMSOutFormat.setText(guiConfig['show_output_format'])
        self.ui.buttonBox.accepted.connect(self.accepted)

    def actualizePreview(self):
        self.__showMatcher__.outputFormat = self.ui.txtMSOutFormat.text()
        self.ui.txtMSPreview.setText(
            self.__showMatcher__.createOutputFile(
                showName = 'The Boys', 
                episodeTitle = 'We Gotta Go Now',
                seasonNumber = 2,
                episodeNumber = 5,
                year = 2019,
                extension = 'mp4'))
    
    def accepted(self):
        guiConfig['show_output_format'] = self.ui.txtMSOutFormat.text()
        guiConfig.saveSettings()
