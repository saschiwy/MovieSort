from .filenameParser import FilenameParser

class Episode():
    
    seasonNumber        = None
    episodeNumber       = None
    episodeString       = None
    file                = None
    estimatedTitle      = None
    isShow              = None
    estimatedTitleFrags = None
    databaseTitle       = None

    def __init__(self):
        self.seasonNumber        = 0
        self.episodeNumber       = 0
        self.episodeString       = ''
        self.file                = FilenameParser()
        self.estimatedTitle      = ''
        self.isShow              = False
        self.estimatedTitleFrags = []
        self.databaseTitle       = ''
    
    def parse(self, name : str):
        self.file.parse(name)

        for s in self.file.parsedNames:
            result = self.file.parseSeasonAndEpisode(s)
            if result[0]:
                self.isShow        = True
                self.seasonNumber  = result[1]
                self.episodeNumber = result[2]
                self.episodeString = result[3]
                break
            else:
                self.estimatedTitleFrags.append(s)
        
        self.estimatedTitle = ' '.join(self.estimatedTitleFrags)
    
    def serialize(self):
        j = dict()
        j['seasonNumber']        = self.seasonNumber       
        j['episodeNumber']       = self.episodeNumber      
        j['episodeString']       = self.episodeString      
        j['file']                = self.file.serialize()        
        j['estimatedTitle']      = self.estimatedTitle     
        j['isShow']              = self.isShow             
        j['estimatedTitleFrags'] = self.estimatedTitleFrags
        j['databaseTitle']       = self.databaseTitle      
        return j

    def deserialize(self, j: dict()):
        self.__init__()
        self.seasonNumber        = j['seasonNumber']       
        self.episodeNumber       = j['episodeNumber']      
        self.episodeString       = j['episodeString']      
        self.file                = FilenameParser()
        self.file.deserialize(j['file'])
        self.estimatedTitle      = j['estimatedTitle']     
        self.isShow              = j['isShow']             
        self.estimatedTitleFrags = j['estimatedTitleFrags']
        self.databaseTitle       = j['databaseTitle']      

class Season():
    episodes     = None
    seasonNumber = None

    def __init__(self):
        self.episodes     = []
        self.seasonNumber = 0
    
    def serialize(self):
        j   = dict()
        arr = []

        j['seasonNumber']   = self.seasonNumber
        for episode in self.episodes:
            arr.append(episode.serialize())
        j['episodes']       = arr
        return j

    def deserialize(self, j: dict()):
        self.__init__()
        self.seasonNumber = j['seasonNumber']
        for e in j['episodes']:
            episode = Episode()
            episode.deserialize(e)
            self.episodes.append(episode)

class TvShow():
    seasons           = None
    estimatedTitle    = None
    firstAirYear      = None
    databaseId        = None
    databaseTitle     = None

    def __init__(self):
        self.seasons           = dict()
        self.estimatedTitle    = ''
        self.firstAirYear      = 1900
        self.databaseId        = 0
        self.databaseTitle     = ''

    def checkAndAddEpisode(self, episode : Episode()):
        if not episode.isShow:
            return False

        # Create new show
        if self.estimatedTitle == '':
            self.estimatedTitle = episode.estimatedTitle
        
        # Episode does not match to show
        elif self.estimatedTitle != episode.estimatedTitle:
            return False

        # Create new Season        
        if episode.seasonNumber not in self.seasons:
            season = Season()
            season.seasonNumber                = episode.seasonNumber
            self.seasons[episode.seasonNumber] = season

        self.seasons[episode.seasonNumber].episodes.append(episode)
        return True

    def serialize(self):
        j = dict()
        j['estimatedTitle'] = self.estimatedTitle 
        j['firstAirYear']   = self.firstAirYear   
        j['databaseId']     = self.databaseId     
        j['databaseTitle']  = self.databaseTitle  

        arr = []
        for season in self.seasons.values():
            arr.append(season.serialize())
        j['seasons'] = arr
        return j
    
    def deserialize(self, j : dict()):
        self.__init__()
        self.estimatedTitle = j['estimatedTitle'] 
        self.firstAirYear   = j['firstAirYear']   
        self.databaseId     = j['databaseId']     
        self.databaseTitle  = j['databaseTitle']  

        for s in j['seasons']:
            season = Season()
            season.deserialize(s)
            self.seasons[season.seasonNumber] = season
