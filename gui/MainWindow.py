import sys
from os.path import join, dirname, abspath

from qtpy import uic
from qtpy.QtCore import Slot, Signal, Qt, QEventLoop
from qtpy.QtWidgets import QApplication, QMainWindow, QMessageBox, QTreeWidgetItem, QTableWidget, QHeaderView, QFileDialog, QTableWidgetItem

import qtmodern.styles
import qtmodern.windows

from MovieSettings import MovieSettingsWindow
from ShowSettings import ShowSettingsWindow
from GeneralSettings import GeneralSettingsWindow
from MovieSelection import MovieSelectionWindow
from movieMatcher import MovieMatcherTMDb
from episodeMatcher import EpisodeMatcherTMDb
from guiConfig import guiConfig
from fops import getFileList
from movie import Movie

_UI = join(dirname(abspath(__file__)), 'MainWindow.ui')

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi(_UI, self)  # Load the ui into self

        self.actionLight.triggered.connect(self.lightTheme)
        self.actionDark.triggered.connect(self.darkTheme)
        self.actionMovie_Settings.triggered.connect(self.openMovieSettings)
        self.actionShow_Settings.triggered.connect(self.openShowSettings)
        self.actionGeneral_Settings.triggered.connect(self.openGeneralSettings)
        self.actionExit.triggered.connect(self.close)
        self.btnMovieChoseFolder.clicked.connect(self.choseMovieFolder)
        self.btnMovieMatch.clicked.connect(self.matchMovies)
        self.btnMovieClear.clicked.connect(self.clearMovies)
        self.btnMovieMove.clicked.connect(self.moveMovies)
        self.btnShowChoseFolder.clicked.connect(self.choseShowFolder)
        self.btnShowMatch.clicked.connect(self.matchShows)
        self.btnShowClear.clicked.connect(self.clearShows)
        self.btnShowMove.clicked.connect(self.moveShows)

        self.tableShowOutput.horizontalHeader().setVisible(True)
        self.tableShowOutput.verticalHeader().setVisible(True)
        self.tableShowInput.horizontalHeader().setVisible(True)
        self.tableShowInput.verticalHeader().setVisible(True)
        self.tableMovieOutput.horizontalHeader().setVisible(True)
        self.tableMovieOutput.verticalHeader().setVisible(True)
        self.tableMovieInput.horizontalHeader().setVisible(True)
        self.tableMovieInput.verticalHeader().setVisible(True)

        self.movieMatcher = MovieMatcherTMDb('./')

    def update_progress(self, progress):
        self.progressBar.setValue(progress)

    def lightTheme(self):
        qtmodern.styles.light(QApplication.instance())

    def darkTheme(self):
        qtmodern.styles.dark(QApplication.instance())
    
    def openMovieSettings(self):
        mw = qtmodern.windows.ModernWindow(MovieSettingsWindow())
        mw.show()
    
    def openShowSettings(self):
        mw = qtmodern.windows.ModernWindow(ShowSettingsWindow())
        mw.show()

    def openGeneralSettings(self):
        mw = qtmodern.windows.ModernWindow(GeneralSettingsWindow())
        mw.show()
    
    def choseMovieFolder(self):
        folder  = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        files   = getFileList(folder, guiConfig["ignore_pattern"])
        
        self.clearMovies()
        self.movieMatcher.outputFormat = guiConfig["movie_output_format"]
        self.movieMatcher.rootFolder   = folder
        self.movieMatcher.setFiles(files)

        r = 0
        self.tableMovieInput.setRowCount(len(self.movieMatcher.movieData.keys()))
        for movie in self.movieMatcher.movieData.keys():
            self.tableMovieInput.setItem(r, 1, QTableWidgetItem(movie.file.fileName + '.' + movie.file.extension))
            self.tableMovieInput.setItem(r, 0, QTableWidgetItem(movie.file.filepath))
            r += 1

    def matchMovies(self):
        # Get Movie as first param and array with result as second
        # [Movie, [result 1, result 2, ...]]
        possibleMatches = self.movieMatcher.getDatabaseMatches()
        for movie, results in possibleMatches:
            id = self.openMovieSelection(movie, results)
            if id != -1:
                self.movieMatcher.fetchDetails(movie, id)
        
        self.movieMatcher.determineRenaming()
        
        r = 0
        self.tableMovieOutput.clearContents()
        self.tableMovieOutput.setRowCount(len(self.movieMatcher.movieData.keys()))
        for movie in self.movieMatcher.movieData.keys():
            if movie.databaseId != -1:
                self.tableMovieOutput.setItem(r, 0, QTableWidgetItem(movie.databaseTitle))
                self.tableMovieOutput.setItem(r, 1, QTableWidgetItem(str(movie.databaseYear)))
                self.tableMovieOutput.setItem(r, 2, QTableWidgetItem(movie.file.targetFileName))
            r += 1
    
    def clearMovies(self):
        self.movieMatcher.__init__('./')
        self.tableMovieInput.clearContents()
        self.tableMovieOutput.clearContents()
        self.tableMovieInput.setRowCount(0)
        self.tableMovieOutput.setRowCount(0)

    def moveMovies(self):
        pass

    def choseShowFolder(self):
        folder = str(QFileDialog.getExistingDirectory(self, "Select Directory"))

    def matchShows(self):
        pass
    
    def clearShows(self):
        pass

    def moveShows(self):
        pass

    def openMovieSelection(self, movie : Movie(), result : list()):
        select = MovieSelectionWindow(movie.file.fullNameAndPath, result)
        select.setWindowModality(Qt.WindowModal)
        mw = qtmodern.windows.ModernWindow(select)
        mw.setWindowModality(Qt.WindowModal)
        mw.show()

        # This loop will wait for the window is destroyed
        loop = QEventLoop()
        select.finished.connect(loop.quit)
        loop.exec()
            
        return select.acceptedId