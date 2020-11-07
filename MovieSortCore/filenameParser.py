class  FilenameParser():
    '''
    A Filename parser determines words or symbols in a string.
    After parsing one can obtain an array of parsed words. The 
    class also ignores some words which are known as not useful
    '''

    splitter = ['.', '-', '_', ' ']
    cutter   = [ 'german', 'english', '720p', '1080p', '2160p', 'web' , 'x264', 'h265',
                 'hdtv', 'xvid', 'french', 'spanish', 'italian', 'h264', 'mkv', 'avi',
                 'mp4']
    ignores  = ['']
    
    filepath        = None
    fileName        = None
    fullNameAndPath = None
    extension       = None
    parsedNames     = None
    targetFileName  = None

    def __init__(self):
        self.filepath        = ''
        self.fileName        = ''
        self.fullNameAndPath = ''
        self.extension       = ''
        self.targetFileName  = ''
        self.parsedNames     = []

    def __splitWords__ (self, string, delimiterList = splitter):
        result = [string]
        
        for delimiter in delimiterList:
            resultNew = []
            for r in result:
                splitted = r.split(delimiter)
                for s in splitted:
                   resultNew.append(s)
            
            result = resultNew
        return result

    def parse(self, fullNameAndPath : str, rootFolder: str):
        fullNameAndPath = fullNameAndPath.replace("\\", "/")
        self.fullNameAndPath = fullNameAndPath
        i = fullNameAndPath.rfind('/')
        if i != -1:
            self.filepath = fullNameAndPath[:i+1]
            self.fileName = fullNameAndPath[i+1:]
        else:
            self.fileName = fullNameAndPath
        
        i = self.fileName.rfind(".")
        if i != -1:
            self.extension = self.fileName[i+1:]
            self.fileName  = self.fileName[:i]

        self.parsedNames = []
        splitted = self.__splitWords__ (self.fullNameAndPath.replace(rootFolder, ''))
        for s in splitted:
            if s.lower() in self.ignores:
                continue

            self.parsedNames.append(s)
        return
    
    # Valid Format 's%%e%%'
    def parseSeasonAndEpisode (self, string : str):
        string = string.lower()
        s = string.find("s")
        e = string.find("e")

        if s == -1 or e == -1:
            return [False, -1, -1, '']

        season  = string[s+1:e]
        episode = string[e+1:]
        if not season.isnumeric() or not episode.isnumeric():
            return [False, -1, -1, '']

        return [True, int(season), int(episode), string]
    
    def serialize(self):
        j = dict()

        j['filepath']        = self.filepath       
        j['fileName']        = self.fileName       
        j['fullNameAndPath'] = self.fullNameAndPath
        j['extension']       = self.extension      
        j['parsedNames']     = self.parsedNames    
        j['targetFileName']  = self.targetFileName 

        return j

    def deserialize(self, j : dict()):
        self.__init__()
        self.filepath        = j['filepath']        
        self.fileName        = j['fileName']        
        self.fullNameAndPath = j['fullNameAndPath'] 
        self.extension       = j['extension']       
        self.parsedNames     = j['parsedNames']     
        self.targetFileName  = j['targetFileName']  

        return j