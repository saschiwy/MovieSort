import sys
from os.path import join, dirname, abspath

from qtpy import uic
from qtpy.QtCore import Slot, QThread, Signal
from qtpy.QtWidgets import QApplication, QDialog

import qtmodern.styles
import qtmodern.windows

_UI = join(dirname(abspath(__file__)), 'CustomEnter.ui')

class CustomEnterWindow(QDialog):

    result = None
    def __init__(self, numbersOnly : bool):
        QDialog.__init__(self)
        uic.loadUi(_UI, self)  # Load the ui into self    
        self.btnOk.accepted.connect(self.accepted)

        if numbersOnly:
            self.txtId.setInputMask("99999999")

    def accepted(self):
        self.result = self.txtId.text()
