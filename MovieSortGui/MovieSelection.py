import sys, os, json, requests

from qtpy import QtGui
from qtpy.QtCore import Slot, QThread, Signal, Qt, QEventLoop
from qtpy.QtWidgets import QApplication, QDialog, QListWidgetItem, QGraphicsPixmapItem, QGraphicsScene, QGraphicsView, QTableWidgetItem
from qtpy.QtGui import QPixmap

import qtmodern.styles
import qtmodern.windows

from tmdbv3api import Movie, TV


from .CustomEnter import CustomEnterWindow
from .Ui_MovieSelection import Ui_MovieSelection

class MovieSelectionWindow(QDialog):
    
    __scene__         = None
    __poster_url__    = 'https://image.tmdb.org/t/p/original'
    __possibilities__ = None
    acceptedId        = -1

    def __init__(self, oFile, possibilities):
        self.acceptedId = -1
        QDialog.__init__(self)
        
        self.ui = Ui_MovieSelection()
        self.ui.setupUi(self)
        
        self.ui.btnEnterId.clicked.connect(self.enterId)
        self.ui.btnEnterTitle.clicked.connect(self.enterTitle)
        self.ui.btnAccept.clicked.connect(self.accept)

        self.ui.tablePossibilities.horizontalHeader().setVisible(True)
        self.ui.tablePossibilities.verticalHeader().setVisible(True)
        self.ui.tablePossibilities.cellClicked.connect(self.selectionChanged)
        self.ui.lblOriginalFile.setText(oFile)

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
        self.ui.graphicsView.setScene(self.__scene__)
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
            self.ui.graphicsView.fitInView(self.__scene__.sceneRect(), mode=Qt.KeepAspectRatio)
            self.ui.graphicsView.show()
    
    def actualizeTable(self):
        self.ui.tablePossibilities.clearContents()

        r = 0
        for p in self.__possibilities__:
            if 'title' not in p.__dict__ or 'release_date' not in p.__dict__:
                self.__possibilities__.remove(p)
                continue
            self.ui.tablePossibilities.setRowCount(r + 1)
            self.ui.tablePossibilities.setItem(r, 0, QTableWidgetItem(p.title))
            self.ui.tablePossibilities.setItem(r, 1, QTableWidgetItem(p.release_date[:4]))
            r += 1
        
        self.ui.tablePossibilities.clearSelection()
    
    def selectionChanged(self, row, column):
        self.ui.txtOverview.clear()
        self.ui.txtOverview.appendPlainText(self.__possibilities__[row].overview)
        self.ui.lblTitle.setText(self.__possibilities__[row].title + ' (' + 
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
        select.ui.txtId.setFocus()

        loop = QEventLoop()
        select.finished.connect(loop.quit)
        loop.exec()

        if select.result != None and select.result.isdecimal(): 
            self.acceptedId = int(select.result)
            self.close()

    def __enterTitleWindow__(self, search):
        select = CustomEnterWindow(False)
        select.setWindowModality(Qt.WindowModal)
        mw = qtmodern.windows.ModernWindow(select)
        mw.setWindowModality(Qt.WindowModal)
        mw.show()
        select.ui.txtId.setFocus()

        loop = QEventLoop()
        select.finished.connect(loop.quit)
        loop.exec()
        
        if select.result != None:
            self.__possibilities__ = search(select.result)
            self.actualizeTable()

    def enterTitle(self):
        self.__enterTitleWindow__(Movie().search)

    def accept(self):
        self.acceptedId = self.__possibilities__[self.ui.tablePossibilities.currentRow()].id
        self.close()

class ShowSelectionWindow(MovieSelectionWindow):
    def __init__(self, showTitle, possibilities):
        MovieSelectionWindow.__init__(self, showTitle, possibilities)

    def enterTitle(self):
        self.__enterTitleWindow__(TV().search)

    
    def actualizeTable(self):
        self.ui.tablePossibilities.clearContents()
        r = 0
        for p in self.__possibilities__:
            if 'first_air_date' not in p.__dict__ or 'name' not in p.__dict__:
                self.__possibilities__.remove(p)
                continue
            print(p.__dict__)
            self.ui.tablePossibilities.setRowCount(r + 1)
            self.ui.tablePossibilities.setItem(r, 0, QTableWidgetItem(p.name))
            self.ui.tablePossibilities.setItem(r, 1, QTableWidgetItem(p.first_air_date[:4]))
            r += 1
        
        self.ui.tablePossibilities.clearSelection()

    def selectionChanged(self, row, column):
        self.ui.txtOverview.clear()
        self.ui.txtOverview.appendPlainText(self.__possibilities__[row].overview)
        self.ui.lblTitle.setText(self.__possibilities__[row].name + ' (' + 
            self.__possibilities__[row].first_air_date[:4] + ')')
        if self.__possibilities__[row].poster_path != None:
            self.showImage(self.__possibilities__[row].poster_path)
        else:
            self.removeImage()
