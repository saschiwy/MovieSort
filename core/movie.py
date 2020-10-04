
import datetime
from .filenameParser import FilenameParser

class Movie():
    
    file                = None
    estimatedTitle      = None
    estimatedTitleFrags = None
    databaseTitle       = None
    databaseId          = None
    databaseYear        = None
    estimatedYear       = None

    def __init__(self):
        self.file                = FilenameParser()
        self.estimatedTitle      = ''
        self.estimatedTitleFrags = []
        self.databaseTitle       = ''
        self.databaseYear        = 1900
        self.databaseId          = 0
        self.estimatedYear       = 1900
    
    def __isYear__(self, string : str):
        if not string.isdecimal():
            return [False, 0]
        
        y = int(string)
        if y > 1900 and y <= datetime.datetime.now().year:
            return [True, y]
        
        return [False, 0]

    def parse(self, name : str, rootFolder):
        self.file.parse(name, rootFolder)

        for s in self.file.parsedNames:
            result = self.__isYear__(s)
            
            if result[0]:
                self.estimatedYear = result[1]
                break
            
        for s in self.file.parsedNames:
            if s.lower() in self.file.cutter:
                break
            self.estimatedTitleFrags.append(s)
            
        self.estimatedTitle      = ' '.join(self.estimatedTitleFrags)

    def serialize(self):
        j = dict()
        j['file']                = self.file.serialize()        
        j['estimatedTitle']      = self.estimatedTitle     
        j['estimatedTitleFrags'] = self.estimatedTitleFrags
        j['databaseTitle']       = self.databaseTitle      
        j['databaseYear']        = self.databaseYear      
        j['databaseId']          = self.databaseId
        j['estimatedYear']       = self.estimatedYear
        return j

    def deserialize(self, j: dict()):
        self.__init__()
        self.file                = FilenameParser()
        self.file.deserialize(j['file'])
        self.estimatedTitle      = j['estimatedTitle']     
        self.estimatedTitleFrags = j['estimatedTitleFrags']
        self.databaseTitle       = j['databaseTitle']    
        self.estimatedYear       = j['estimatedYear']    
        self.databaseYear        = j['databaseYear']    
        self.databaseId          = j['databaseId']    