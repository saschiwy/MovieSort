import sys, os, json, requests
from os.path import join, dirname, abspath

from qtpy import uic, QtGui
from qtpy.QtCore import Slot, QThread, Signal, Qt, QEventLoop
from qtpy.QtWidgets import QApplication, QDialog, QListWidgetItem, QGraphicsPixmapItem, QGraphicsScene, QGraphicsView, QTableWidgetItem
from qtpy.QtGui import QPixmap

import qtmodern.styles
import qtmodern.windows

from CustomEnter import CustomEnterWindow
from tmdbv3api import Movie

_UI = join(dirname(abspath(__file__)), 'MovieSelection.ui')

class MovieSelectionWindow(QDialog):
    
    __scene__         = None
    __poster_url__    = 'https://image.tmdb.org/t/p/original'
    __possibilities__ = None
    acceptedId        = -1

    def __init__(self, oFile, possibilities):
        self.acceptedId = -1
        QDialog.__init__(self)
        uic.loadUi(_UI, self)

        self.btnEnterId.clicked.connect(self.enterId)
        self.btnEnterTitle.clicked.connect(self.enterTitle)
        self.btnAccept.clicked.connect(self.accept)

        self.tablePossibilities.horizontalHeader().setVisible(True)
        self.tablePossibilities.verticalHeader().setVisible(True)
        self.tablePossibilities.cellClicked.connect(self.selectionChanged)
        self.lblOriginalFile.setText(oFile)

        self.__possibilities__ = possibilities
        self.actualizeTable()
        
    def showImage(self, posterPath: str):
        self.removeImage()
        imgData = requests.get(self.__poster_url__ + posterPath)
        pix = QPixmap()
        pix.loadFromData(imgData.content)
        item = QGraphicsPixmapItem(pix)
        self.__scene__ = QGraphicsScene(self)
        self.__scene__.addItem(item)
        self.graphicsView.setScene(self.__scene__)
        self.resizeImage()
    
    def removeImage(self):
        if self.__scene__ != None:
            self.__scene__.clear()
        self.__scene__ = None

    def resizeEvent(self, event):
        QDialog.resizeEvent(self, event)
        self.resizeImage()
    
    def resizeImage(self):
        if(self.__scene__ != None):
            self.graphicsView.fitInView(self.__scene__.sceneRect(), mode=Qt.KeepAspectRatio)
            self.graphicsView.show()
    
    def actualizeTable(self):
        self.tablePossibilities.clearContents()
        self.tablePossibilities.setRowCount(len(self.__possibilities__))

        r = 0
        for p in self.__possibilities__:
            self.tablePossibilities.setItem(r, 0, QTableWidgetItem(p.title))
            self.tablePossibilities.setItem(r, 1, QTableWidgetItem(p.release_date[:4]))
            r += 1
        
        self.tablePossibilities.clearSelection()
    
    def selectionChanged(self, row, column):
        self.txtOverview.clear()
        self.txtOverview.appendPlainText(self.__possibilities__[row].overview)
        self.lblTitle.setText(self.__possibilities__[row].title + ' (' + 
            self.__possibilities__[row].release_date[:4] + ')')
        if self.__possibilities__[row].poster_path != None:
            self.showImage(self.__possibilities__[row].poster_path)
        else:
            self.removeImage()
    
    def enterId(self):
        select = CustomEnterWindow(True)
        select.setWindowModality(Qt.WindowModal)
        mw = qtmodern.windows.ModernWindow(select)
        mw.setWindowModality(Qt.WindowModal)
        mw.show()

        loop = QEventLoop()
        select.finished.connect(loop.quit)
        loop.exec()

        if select.result != None and select.result.isdecimal(): 
            self.acceptedId = int(select.result)
            self.close()

    def enterTitle(self):
        select = CustomEnterWindow(False)
        select.setWindowModality(Qt.WindowModal)
        mw = qtmodern.windows.ModernWindow(select)
        mw.setWindowModality(Qt.WindowModal)
        mw.show()

        loop = QEventLoop()
        select.finished.connect(loop.quit)
        loop.exec()
        
        if select.result != None:
            self.__possibilities__ = Movie().search(select.result)
            self.actualizeTable()

    def accept(self):
        self.acceptedId = self.__possibilities__[self.tablePossibilities.currentRow()].id
        self.close()

