from tmdbv3api import TMDb
from tmdbv3api import Movie as tmbdMovie

from .fops import removeDisallowedFilenameChars
from .movie import Movie

class MovieMatcher():
    
    files        = None
    movieData    = dict()
    outputFormat = "./%t (%y)/%t (%y).%x"
    rootFolder   = None

    def __init__(self, rootFolder: str):
        self.files        = []
        self.movieData    = dict()
        self.rootFolder   = rootFolder
    
    def __parseMovies__(self):
        for file in self.files:
            m = Movie()
            m.parse(file, self.rootFolder)
            self.movieData[m] = None

    def setFiles(self, files : []):
        self.files = files
        self.__parseMovies__()

    # Allowed special Character
    # %t   - Movie Title
    # %y   - Year
    # %x   - File Extension
    def createOutputFile(self,  movieName : str, 
                                year : int,
                                extension : str
                                ):
        return self.outputFormat \
                .replace('%t', movieName) \
                .replace('%x', extension) \
                .replace('%y', str(year))
    
    def _recursiveSearch_(self, searchArray :[], searchObj = tmbdMovie()):
        result = []

        while len(result) == 0 and len(searchArray) > 0:
            searchString = ' '.join(searchArray)
            searchArray  = searchArray[:len(searchArray) - 1]
            result = searchObj.search(searchString)
        return result
    
    def moveFiles(self, overwrite : bool):
        for movie in self.movieData.keys():
            movie.move(overwrite)

class MovieMatcherTMDb(MovieMatcher):

    def __init__(self, rootFolder: str):
        MovieMatcher.__init__(self, rootFolder)
        
    # Get matches in TMDb for all movies in dict
    def getDatabaseMatches(self):
        result = []
        for movie in self.movieData.keys():
            result.append([movie, self._recursiveSearch_(movie.estimatedTitleFrags)])
        return result
    
    def fetchDetails(self, movie : Movie, id):
        details = tmbdMovie().details(id)
        movie.databaseTitle   = details.title
        if 'release_date' in details.__dict__ and len(details.release_date) >= 4:
            movie.databaseYear    = int(details.release_date[:4])
        else:
            movie.databaseYear    = 0
        movie.databaseId      = id
        self.movieData[movie] = details
    
    def determineRenaming(self):
        for movie in self.movieData.keys():
            if movie.databaseTitle == '':
                continue

            target = self.createOutputFile (movie.databaseTitle, 
                    movie.databaseYear,
                    movie.file.extension)

            movie.setTarget(removeDisallowedFilenameChars(target))