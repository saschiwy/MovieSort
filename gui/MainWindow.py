import sys, os, shutil
from os.path import join, dirname, abspath
import webbrowser

#from qtpy import uic
from qtpy.QtCore import Slot, Signal, Qt, QEventLoop
from qtpy.QtWidgets import QApplication, QMainWindow, QMessageBox, QTreeWidgetItem, QTableWidget, QHeaderView, QFileDialog, QTableWidgetItem

import qtmodern.styles
import qtmodern.windows

from MovieSettings import MovieSettingsWindow
from ShowSettings import ShowSettingsWindow
from GeneralSettings import GeneralSettingsWindow
from MovieSelection import MovieSelectionWindow, ShowSelectionWindow
from movieMatcher import MovieMatcherTMDb
from episodeMatcher import EpisodeMatcherTMDb
from guiConfig import guiConfig
from fops import getFileList
from movie import Movie
from tvShow import TvShow, Episode
from Ui_MainWindow import Ui_MainWindow

#_UI = join(dirname(abspath(__file__)), 'MainWindow.ui')

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        #uic.loadUi(_UI, self)  # Load the ui into self
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.actionLight.triggered.connect(self.lightTheme)
        self.ui.actionDark.triggered.connect(self.darkTheme)
        self.ui.actionMovie_Settings.triggered.connect(self.openMovieSettings)
        self.ui.actionShow_Settings.triggered.connect(self.openShowSettings)
        self.ui.actionGeneral_Settings.triggered.connect(self.openGeneralSettings)
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionDonate.triggered.connect(self.donate)
        self.ui.btnMovieChoseFolder.clicked.connect(self.choseMovieFolder)
        self.ui.btnMovieMatch.clicked.connect(self.matchMovies)
        self.ui.btnMovieClear.clicked.connect(self.clearMovies)
        self.ui.btnMovieMove.clicked.connect(self.moveMovies)
        self.ui.btnShowChoseFolder.clicked.connect(self.choseShowFolder)
        self.ui.btnShowMatch.clicked.connect(self.matchShows)
        self.ui.btnShowClear.clicked.connect(self.clearShows)
        self.ui.btnShowMove.clicked.connect(self.moveShows)

        self.ui.tableShowOutput.horizontalHeader().setVisible(True)
        self.ui.tableShowOutput.verticalHeader().setVisible(True)
        self.ui.tableShowInput.horizontalHeader().setVisible(True)
        self.ui.tableShowInput.verticalHeader().setVisible(True)
        self.ui.tableMovieOutput.horizontalHeader().setVisible(True)
        self.ui.tableMovieOutput.verticalHeader().setVisible(True)
        self.ui.tableMovieInput.horizontalHeader().setVisible(True)
        self.ui.tableMovieInput.verticalHeader().setVisible(True)

        self.movieMatcher    = MovieMatcherTMDb('./')
        self.episodeMatcher  = EpisodeMatcherTMDb('./')

    def update_progress(self, progress):
        self.ui.progressBar.setValue(progress)

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
        self.ui.tableMovieInput.setRowCount(len(self.movieMatcher.movieData.keys()))
        for movie in self.movieMatcher.movieData.keys():
            self.ui.tableMovieInput.setItem(r, 1, QTableWidgetItem(movie.file.fileName + '.' + movie.file.extension))
            self.ui.tableMovieInput.setItem(r, 0, QTableWidgetItem(movie.file.filepath))
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
        self.ui.tableMovieOutput.clearContents()
        self.ui.tableMovieOutput.setRowCount(len(self.movieMatcher.movieData.keys()))
        for movie in self.movieMatcher.movieData.keys():
            if movie.databaseId != -1:
                self.ui.tableMovieOutput.setItem(r, 0, QTableWidgetItem(movie.databaseTitle))
                self.ui.tableMovieOutput.setItem(r, 1, QTableWidgetItem(str(movie.databaseYear)))
                self.ui.tableMovieOutput.setItem(r, 2, QTableWidgetItem(movie.file.targetFileName))
            r += 1
    
    def clearMovies(self):
        self.movieMatcher.__init__('./')
        self.ui.tableMovieInput.clearContents()
        self.ui.tableMovieOutput.clearContents()
        self.ui.tableMovieInput.setRowCount(0)
        self.ui.tableMovieOutput.setRowCount(0)
    
    def clearShows(self):
        self.episodeMatcher.__init__('./')
        self.ui.tableShowInput.clearContents()
        self.ui.tableShowOutput.clearContents()
        self.ui.tableShowInput.setRowCount(0)
        self.ui.tableShowOutput.setRowCount(0)

    def moveFiles(self, files : [], overwrite : bool):
        
        num = len(files)
        self.ui.progressBar.setValue(0)

        c=0
        for source, target in files:
            pos       = target.rfind("/")
            targetDir = "./"
            if pos != -1:
                targetDir = target[:pos]

            # check if directory exists or not yet
            if not os.path.exists(targetDir):
                os.makedirs(targetDir)

            if os.path.isfile(target) and overwrite:
                os.remove(target)

            if os.path.exists(targetDir):
                shutil.move(source, target)
            
            c += 1
            self.ui.progressBar.setValue(c * 100 / num)
            

    def moveMovies(self):
        self.moveFiles(self.movieMatcher.matchedFiles, bool(guiConfig['overwrite_files']))
        self.clearMovies()

    def choseShowFolder(self):
        folder = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        files  = getFileList(folder, guiConfig["ignore_pattern"])
        
        self.clearShows()
        self.episodeMatcher.outputFormat = guiConfig["show_output_format"]
        self.episodeMatcher.rootFolder   = folder
        self.episodeMatcher.setFiles(files)

        episodes = self.episodeMatcher.getAllEpisodes()
        
        r = 0
        self.ui.tableShowInput.setRowCount(len(episodes))
        for episode in episodes:
            self.ui.tableShowInput.setItem(r, 1, QTableWidgetItem(episode.file.fileName + '.' + episode.file.extension))
            self.ui.tableShowInput.setItem(r, 0, QTableWidgetItem(episode.file.filepath))
            r += 1

    def matchShows(self):
        # Get Movie as first param and array with result as second
        # [Movie, [result 1, result 2, ...]]
        possibleMatches = self.episodeMatcher.getDatabaseMatches()
        for show, results in possibleMatches:
            id = self.openShowSelection(show, results)
            if id != -1:
                self.episodeMatcher.fetchDetails(show, id)
        
        self.episodeMatcher.determineRenaming()
        
        r = 0
        for show in self.episodeMatcher.tvShows.keys():
            for season in show.seasons.values():
                for episode in season.episodes:
                    self.ui.tableShowOutput.setRowCount(r + 1)
                    if episode.file.targetFileName != '' and show.databaseTitle != '':
                        self.ui.tableShowOutput.setItem(r, 0, QTableWidgetItem(show.databaseTitle))
                        self.ui.tableShowOutput.setItem(r, 1, QTableWidgetItem(show.firstAirYear))
                        self.ui.tableShowOutput.setItem(r, 2, QTableWidgetItem(str(season.seasonNumber)))
                        self.ui.tableShowOutput.setItem(r, 3, QTableWidgetItem(str(episode.episodeNumber)))
                        self.ui.tableShowOutput.setItem(r, 4, QTableWidgetItem(str(episode.databaseTitle)))
                        self.ui.tableShowOutput.setItem(r, 5, QTableWidgetItem(str(episode.file.targetFileName)))
                    r += 1

    def moveShows(self):
        self.moveFiles(self.episodeMatcher.matchedFiles, bool(guiConfig['overwrite_files']))
        self.clearShows()

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

    def openShowSelection(self, show : TvShow(), result : list()):
        select = ShowSelectionWindow(show.estimatedTitle, result)
        select.setWindowModality(Qt.WindowModal)
        mw = qtmodern.windows.ModernWindow(select)
        mw.setWindowModality(Qt.WindowModal)
        mw.show()

        # This loop will wait for the window is destroyed
        loop = QEventLoop()
        select.finished.connect(loop.quit)
        loop.exec()
            
        return select.acceptedId
    
    def donate(self):
        webbrowser.open('https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=JBK73YUVW7MGW&source=url', new = 2)