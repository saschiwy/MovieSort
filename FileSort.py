import sys
sys.path.insert(0, './core')
sys.path.insert(0, './gui')

from tmdbv3api import TMDb

from qtpy.QtWidgets import QApplication
from MainWindow import MainWindow
from guiConfig import guiConfig

import qtmodern.styles
import qtmodern.windows

if __name__ == '__main__':
    TMDb().language = guiConfig['language']
    TMDb().api_key  = 'e24fcd17eff0cfe0064fa7b5cb05b97d'

    app = QApplication(sys.argv)
    qtmodern.styles.dark(app)
    mw = qtmodern.windows.ModernWindow(MainWindow())
    mw.show()

    res = app.exec_()
    sys.exit(res)
    