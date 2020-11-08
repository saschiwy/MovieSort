#!/usr/bin/env python

__author__     = "Sascha Schiwy"
__copyright__  = "Copyright 2020, Sascha Schiwy"
__credits__    = []
__license__    = "GPLv2"
__version__    = "0.0.1"
__maintainer__ = "Sascha Schiwy"
__email__      = "sascha.schiwy@gmail.com"
__status__     = "Alpha"

import sys
sys.path.insert(0, './MovieSortCore')

from tmdbv3api import TMDb

from qtpy.QtWidgets import QApplication
from MovieSortGui import MainWindow, guiConfig

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
    