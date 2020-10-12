from .tvShow import TvShow
from .tvShow import Episode

from tmdbv3api import TMDb
from tmdbv3api import TV
from tmdbv3api import Season

from .fops import removeDisallowedFilenameChars

class EpisodeMatcher():
    
    matchedFiles = None
    files        = None
    tvShows      = dict()
    showDetails  = None
    outputFormat = "./%n (%y)/Season %0s/%n (%y) - S%0sE%0e - %t.%x"

    def __init__(self):
        self.files        = []
        self.tvShows      = dict()
        self.matchedFiles = []

    def __getShows__ (self, files : []):
        self.tvShows = dict()
        
        for file in files:
            epi = Episode()
            epi.parse(file)
            added = False

            if not epi.isShow:
                continue

            for show in self.tvShows.keys():
                if show.checkAndAddEpisode(epi):
                    added = True
                    break
            
            if not added:
                s = TvShow()
                s.checkAndAddEpisode(epi)
                self.tvShows[s] = None

    def setFiles(self, files : []):
        self.__getShows__(files)
        self.files = files

    # Allowed special Character
    # %n   - Show Name
    # %s   - Season Number
    # %0s  - Season Number, Zero Padded [01, 02...]
    # %00s - Season Number, Zero Padded [001, 002...]
    # %e   - Episode Number
    # %0e  - Episode Number, Zero Padded [01, 02...]
    # %00e - Episode Number, Zero Padded [001, 002...]
    # %t   - Episode Title
    # %y   - First Air Year
    # %x   - File Extension
    def createOutputFile(self,  showName : str, 
                                episodeTitle : str,
                                seasonNumber : int,
                                episodeNumber :int,
                                year : int,
                                extension : str
                                ):
        return self.outputFormat \
                .replace('%n', showName) \
                .replace('%t', episodeTitle) \
                .replace('%s', str(seasonNumber)) \
                .replace('%0s', str(seasonNumber).zfill(2)) \
                .replace('%00s', str(seasonNumber).zfill(3)) \
                .replace('%e', str(episodeNumber)) \
                .replace('%0e', str(episodeNumber).zfill(2)) \
                .replace('%00e', str(episodeNumber).zfill(3)) \
                .replace('%x', extension) \
                .replace('%y', str(year))

class EpisodeMatcherTMDb(EpisodeMatcher):

    def __init__(self):
        EpisodeMatcher.__init__(self)
        self.setLanguage('en')
        self.setApiKey('e24fcd17eff0cfe0064fa7b5cb05b97d')

    def setLanguage (self, lang):
        TMDb().language = lang

    def setApiKey (self, apiKey):
        TMDb().api_key  = apiKey
    
    def getDatabaseMatches(self):
        tv     = TV()
        result = []
        
        for show in self.tvShows.keys():
            search = tv.search(show.estimatedTitle)
            result.append([show, search])
        
        return result
    
    def fetchDetails(self, show, id):
        if show not in self.tvShows:
            return False

        # Fetch show information
        details            = TV().details(id)
        self.tvShows[show] = details
        show.firstAirYear  = int(details.first_air_date[:4])
        show.databaseId    = id
        show.databaseTitle = details.obj_name

        # Fetch episode information
        for sNbr, season in show.seasons.items():
            if not self.__seasonAvailable__(sNbr, details):
                continue

            seasonDetails  = Season().details(id, sNbr)
            for episode in season.episodes:
                episodeDetails = None

                # Check if episode exist
                for e in seasonDetails.episodes:
                    if e['episode_number'] == episode.episodeNumber:
                        episodeDetails = e
                        break
            
                if episodeDetails == None:
                    continue

                episode.databaseTitle = episodeDetails['name']
        return True

    def __seasonAvailable__(self, seasonNbr, detail):
        for s in detail.seasons:
            if seasonNbr == s['season_number']:
                return True
        return False
    
    def determineRenaming(self):
        self.matchedFiles = []
        for show in self.tvShows.keys():
            if show.databaseTitle == '':
                continue

            for sNbr, season in show.seasons.items():
                for episode in season.episodes:
                    if episode.databaseTitle == '':
                        continue                    

                    target = self.createOutputFile(show.databaseTitle, 
                                    episode.databaseTitle, sNbr, 
                                    episode.episodeNumber,
                                    show.firstAirYear,
                                    episode.file.extension)
                    
                    target = removeDisallowedFilenameChars(target)
                    
                    episode.file.targetFileName = target
                    self.matchedFiles.append([episode.file.fullNameAndPath, target ])