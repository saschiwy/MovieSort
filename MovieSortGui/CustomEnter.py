from qtpy.QtWidgets import QDialog
from .Ui_CustomEnter import Ui_SetId

class CustomEnterWindow(QDialog):

    result = None
    def __init__(self, numbersOnly : bool):
        QDialog.__init__(self)
        
        self.ui = Ui_SetId()
        self.ui.setupUi(self)

        self.ui.btnOk.accepted.connect(self.accepted)

        if numbersOnly:
            self.ui.txtId.setInputMask("99999999")
            
    def accepted(self):
        self.result = self.ui.txtId.text()
