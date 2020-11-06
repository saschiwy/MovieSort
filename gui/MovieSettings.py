import sys
from time import sleep
from os.path import join, dirname, abspath

from qtpy.QtCore import Slot, QThread, Signal
from qtpy.QtWidgets import QApplication, QDialog

import qtmodern.styles
import qtmodern.windows

from movieMatcher import MovieMatcher
from guiConfig import guiConfig
from Ui_MovieSettings import Ui_Dialog as Ui_MovieSettings

class MovieSettingsWindow(QDialog):

    __movieMatcher__ = MovieMatcher('./')

    def __init__(self):
        QDialog.__init__(self)
        
        self.ui = Ui_MovieSettings()
        self.ui.setupUi(self)

        self.actualizePreview()
        self.ui.txtMSOutFormat.textChanged[str].connect(self.actualizePreview)
        self.ui.txtMSOutFormat.setText(guiConfig['movie_output_format'])
        self.ui.buttonBox.accepted.connect(self.accepted)

    def actualizePreview(self):
        self.__movieMatcher__.outputFormat = self.ui.txtMSOutFormat.text()
        self.ui.txtMSPreview.setText(
            self.__movieMatcher__.createOutputFile(
                'Iron Man 2', 2010, 'mp4'))
    
    def accepted(self):
        guiConfig['movie_output_format'] = self.ui.txtMSOutFormat.text()
        guiConfig.saveSettings()
